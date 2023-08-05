import struct

from zmqbase import ClientBase
from zmq_fallback import ZmqSocket
from twisted.internet import reactor, task
from binascii import unhexlify

import time
import zmq
import bitcoin
import serialize
import error_code


def unpack_error(data):
    value = struct.unpack_from('<I', data, 0)[0]
    return error_code.error_code.name_from_id(value)


def pack_block_index(index):
    if type(index) == str:
        assert len(index) == 32
        return serialize.ser_hash(index)
    elif type(index) == int:
        return struct.pack('<I', index)
    else:
        raise ValueError("Unknown index type")


def spend_checksum(hash, index):
    hash = hash[::-1]
    index_bytes = struct.pack("<I", index)
    assert len(hash) == 32
    assert len(index_bytes) == 4
    combined = index_bytes + hash[4:8]
    value = struct.unpack("<Q", combined)[0]
    # value & (2**n - 1) is the same as value % 2**n
    return value & (2**63 - 1)


class PointIdent:
    Output = False
    Spend = True


class LibbitcoinClient(ClientBase):
    valid_messages = [
        'fetch_block_header',
        'fetch_history',
        'fetch_history2',
        'subscribe',
        'fetch_last_height',
        'fetch_transaction',
        'fetch_txpool_transaction',
        'fetch_spend',
        'fetch_transaction_index',
        'fetch_block_transaction_hashes',
        'fetch_block_height',
        'fetch_stealth',
        'total_connections',
        'update',
        'renew',
        'broadcast_transaction',
        'validate'
    ]

    def __init__(self, address, public_key=None, log=None, heartbeat_port=9092):
        ClientBase.__init__(self, address)
        self.address = address
        self.public_key = public_key
        self.connected = False
        self.log = log
        self.subscribed = 0
        self.listen_heartbeat(heartbeat_port)
        task.LoopingCall(self.renew_subscriptions).start(120, now=False)

    def listen_heartbeat(self, port):
        def timeout():
            self.connected = False
            if self.log:
                self.log.critical("Libbitcoin server offline")
            s.close()
            self.listen_heartbeat(port)

        def frame_received(frame, more):
            t.reset(10)
            if not self.connected:
                self.connected = True
                if self.log:
                    self.log.info("Libbitcoin server online")

        t = reactor.callLater(10, timeout)

        s = ZmqSocket(frame_received, 3, type=zmq.SUB)
        s.connect(self.address[:len(self.address) - 4] + str(port), self.public_key)

    def renew_subscriptions(self):
        for address in self._subscriptions["address"]:
            for cb in self._subscriptions["address"][address]["callbacks"]:
                self.subscribed -= 1
                if self._subscriptions["address"][address]["expiration"] > time.time():
                    self.renew_address(address)
                else:
                    self._subscriptions["address"].pop(address)

    # Command implementations
    def renew_address(self, address, cb=None):
        address_version, address_hash = \
            bitcoin.bc_address_to_hash_160(address)
        # prepare parameters
        data = struct.pack('B', 0)          # type = address
        data += struct.pack('B', 160)       # bitsize
        data += address_hash                # address

        # run command
        self.send_command('address.renew', data, cb)

    def subscribe_address(self, address, notification_cb=None, cb=None):
        address_version, address_hash = \
            bitcoin.bc_address_to_hash_160(address)
        # Prepare parameters. Use full prefix for now.
        # Type. 0 is address, 1 is stealth.
        data = struct.pack('B', 0)
        # Bitsize
        data += struct.pack('B', 160)
        # Hash bytes
        data += address_hash

        # run command
        self.send_command('address.subscribe', data, cb)
        if notification_cb:
            subscriptions = self._subscriptions['address']
            if address not in subscriptions:
                subscriptions[address] = {
                    "expiration": time.time() + 86400,
                    "callbacks": []
                }
            subscriptions = self._subscriptions['address'][address]
            if notification_cb not in subscriptions["callbacks"]:
                subscriptions["callbacks"].append(notification_cb)

    def subscribe_prefix(self, prefix, notification_cb=None, cb=None):
        # prefix = obelisk.Binary.from_string("1011110101")
        # https://wiki.unsystem.net/en/index.php/DarkWallet/Subscriber

        # Prepare parameters.
        # Type. 0 is address, 1 is stealth.
        data = struct.pack('B', 0)
        # Bitsize
        data += struct.pack('B', prefix.size)
        # Blocks

        # run command
        self.send_command('address.subscribe', data, cb)
        data += prefix.blocks

    def subscribe_stealth(self, prefix, notification_cb=None, cb=None):
        # prefix = obelisk.Binary.from_string("1011110101")
        # https://wiki.unsystem.net/en/index.php/DarkWallet/Subscriber

        # Prepare parameters.
        # Type. 0 is address, 1 is stealth.
        data = struct.pack('B', 1)
        # Bitsize
        data += struct.pack('B', prefix.size)
        # Blocks

        # run command
        self.send_command('address.subscribe', data, cb)
        data += prefix.blocks

    def unsubscribe_address(self, address, subscribed_cb, cb=None):
        address_version, address_hash = \
            bitcoin.bc_address_to_hash_160(address)

        subscriptions = self._subscriptions['address']
        if address in subscriptions:
            if subscribed_cb in subscriptions[address]["callbacks"]:
                subscriptions[address]["callbacks"].remove(subscribed_cb)
                if len(subscriptions[address]["callbacks"]) == 0:
                    subscriptions.pop(address)
        if cb:
            cb(None, address)
        if self.subscribed > 0:
            self.subscribed -= 1

    def fetch_block_header(self, index, cb):
        """Fetches the block header by height."""
        data = pack_block_index(index)
        self.send_command('blockchain.fetch_block_header', data, cb)

    def fetch_history2(self, address, cb, from_height=0):
        """Fetches history for an address. cb is a callback which
        accepts an error code, and a list of rows consisting of:

            id (obelisk.PointIdent.output or spend)
            point (hash and index)
            block height
            value / checksum

        If the row is for an output then the last item is the value.
        Otherwise it is a checksum of the previous output point, so
        spends can be matched to the rows they spend.
        Use spend_checksum(output_hash, output_index) to compute
        output point checksums."""
        address_version, address_hash = \
            bitcoin.bc_address_to_hash_160(address)

        # prepare parameters
        data = struct.pack('B', address_version)    # address version
        data += address_hash                        # address
        data += struct.pack('<I', from_height)      # from_height

        # run command
        self.send_command('address.fetch_history2', data, cb)

    def fetch_history(self, address, cb, from_height=0):
        """Fetches the output points, output values, corresponding input point
        spends and the block heights associated with a Bitcoin address.
        The returned history is a list of rows with the following fields:

            output
            output_height
            value
            spend
            spend_height

        If an output is unspent then the input spend hash will be equivalent
        to null_hash.

        Summing the list of values for unspent outpoints gives the balance
        for an address."""
        address_version, address_hash = \
            bitcoin.bc_address_to_hash_160(address)

        # prepare parameters
        data = struct.pack('B', address_version)    # address version
        data += address_hash[::-1]                  # address
        data += struct.pack('<I', from_height)      # from_height

        # run command
        self.send_command('address.fetch_history', data, cb)

    def fetch_last_height(self, cb):
        """Fetches the height of the last block in our blockchain."""
        self.send_command('blockchain.fetch_last_height', cb=cb)

    def fetch_transaction(self, tx_hash, cb):
        """Fetches a transaction by hash from the blockchain."""
        data = serialize.ser_hash(tx_hash)
        self.send_command('blockchain.fetch_transaction', data, cb)

    def fetch_txpool_transaction(self, tx_hash, cb):
        """Fetches a transaction by hash from the txpool."""
        data = serialize.ser_hash(tx_hash)
        self.send_command('transaction_pool.fetch_transaction', data, cb)

    def fetch_spend(self, outpoint, cb):
        """Fetches a corresponding spend of an output."""
        data = outpoint.serialize()
        self.send_command('blockchain.fetch_spend', data, cb)

    def fetch_transaction_index(self, tx_hash, cb):
        """Fetch the block height that contains a transaction and its index
        within a block."""
        data = serialize.ser_hash(tx_hash)
        self.send_command(
            'blockchain.fetch_transaction_index', data, cb
        )

    def fetch_block_transaction_hashes(self, tx_hash, cb):
        """Fetches list of transaction hashes in a block by block hash."""
        data = serialize.ser_hash(tx_hash)
        self.send_command(
            'blockchain.fetch_block_transaction_hashes', data, cb
        )

    def fetch_block_height(self, blk_hash, cb):
        """Fetches the height of a block given its hash."""
        data = serialize.ser_hash(blk_hash)
        self.send_command('blockchain.fetch_block_height', data, cb)

    def fetch_stealth(self, prefix, cb, from_height=0):
        """Fetch possible stealth results. These results can then be iterated
        to discover new payments belonging to a particular stealth address.
        This is for recipient privacy.

        The prefix is a special value that can be adjusted to provide
        greater precision at the expense of deniability.

        from_height is not guaranteed to only return results from that
        height, and may also include results from earlier blocks.
        It is provided as an optimisation. All results at and after
        from_height are guaranteed to be returned however."""
        assert len(prefix) >= 1
        number_bits = prefix[0]
        data = struct.pack('<B', number_bits)
        for value in prefix[1:]:
            data += struct.pack('<B', value)
        data += struct.pack('<I', from_height)
        self.send_command('blockchain.fetch_stealth', data, cb)

    def total_connections(self, cb):
        """Fetches the total number of connections."""
        self.send_command('protocol.total_connections', cb=cb)

    def broadcast(self, tx, cb=None):
        """A transaction broadcast function."""
        self.send_command("protocol.broadcast_transaction", unhexlify(tx), cb=cb)

    def validate(self, tx, cb=None):
        """Check if a tx is in the mempool"""
        self.send_command("transaction_pool.validate", unhexlify(tx), cb=cb)

    # receive handlers
    def _on_fetch_block_header(self, data):
        error = unpack_error(data)
        assert len(data[4:]) == 80
        header = data[4:]
        return (error, header)

    def _on_fetch_history2(self, data):
        error = unpack_error(data)
        # parse results
        rows = self.unpack_table("<B32sIIQ", data, 4)
        history = []
        for id, hash, index, height, value in rows:
            if id == 0:
                id = False
            else:
                id = True
            hash = hash[::-1]
            history.append((id, hash, index, height, value))
        return (error, history)

    def _on_fetch_history(self, data):
        error = unpack_error(data)
        # parse results
        rows = self.unpack_table("<32sIIQ32sII", data, 4)
        history = []
        for row in rows:
            o_hash, o_index, o_height, value, s_hash, s_index, s_height = row
            o_hash = o_hash[::-1]
            s_hash = s_hash[::-1]
            if s_index == 4294967295:
                s_hash = None
                s_index = None
                s_height = None
            history.append(
                (o_hash, o_index, o_height, value, s_hash, s_index, s_height))
        return (error, history)

    def _on_fetch_last_height(self, data):
        error = unpack_error(data)
        height = struct.unpack('<I', data[4:])[0]
        return (error, height)

    def _on_fetch_transaction(self, data):
        error = unpack_error(data)
        tx = data[4:]
        return (error, tx)

    def _on_fetch_txpool_transaction(self, data):
        error = unpack_error(data)
        tx = data[4:]
        return (error, tx)

    def _on_fetch_spend(self, data):
        error = unpack_error(data)
        spend = serialize.deser_output_point(data[4:])
        return (error, spend)

    def _on_fetch_transaction_index(self, data):
        error = unpack_error(data)
        height, index = struct.unpack("<II", data[4:])
        return (error, height, index)

    def _on_fetch_block_transaction_hashes(self, data):
        error = unpack_error(data)
        rows = self.unpack_table("32s", data, 4)
        hashes = [row[0][::-1] for row in rows]
        return (error, hashes)

    def _on_fetch_block_height(self, data):
        error = unpack_error(data)
        height = struct.unpack('<I', data[4:])[0]
        return (error, height)

    def _on_fetch_stealth(self, data):
        error = unpack_error(data)
        raw_rows = self.unpack_table("<32s20s32s", data, 4)
        rows = []
        for ephemkey, address, tx_hash in raw_rows:
            ephemkey = ephemkey[::-1]
            address = address[::-1]
            tx_hash = tx_hash[::-1]
            rows.append((ephemkey, address, tx_hash))
        return (error, rows)

    def _on_total_connections(self, data):
        error = unpack_error(data)
        height = struct.unpack('<I', data[4:])[0]
        return (error, height)

    def _on_subscribe(self, data):
        self.subscribed += 1
        error = unpack_error(data)
        if error:
            print "Error subscribing", error
        if not self.subscribed % 1000:
            print "Subscribed ok", self.subscribed
        return (error, True)

    def _on_update(self, data):
        address_version = struct.unpack_from('B', data, 0)[0]
        address_hash = data[1:21]
        address = bitcoin.hash_160_to_bc_address(address_hash, address_version)

        height = struct.unpack_from('I', data, 21)[0]
        block_hash = data[25:57]
        tx = data[57:]

        if address in self._subscriptions['address']:
            for update_cb in self._subscriptions['address'][address]["callbacks"]:
                update_cb(
                    address_version, address_hash, height, block_hash, tx
                )

    def _on_renew(self, data):
        self.subscribed += 1
        error = unpack_error(data)
        if error:
            print "Error subscribing"
        if not self.subscribed % 1000:
            print "Renew ok", self.subscribed
        return (error, True)

    def _on_broadcast_transaction(self, data):
        error = unpack_error(data)
        return (error, data)

    def _on_validate(self, data):
        error = unpack_error(data)
        return (error, data)
