from trezor.crypto.hashlib import sha256
from common import *

from apps.wallet.sign_tx.writers import *
from trezor.messages.SignTx import SignTx


class Bip143:

    def __init__(self):
        self.h_prevouts = HashWriter(sha256)  # todo make private
        self.h_sequence = HashWriter(sha256)  # todo make private
        self.h_outputs = HashWriter(sha256)  # todo make private

    def add_prevouts(self, txi: TxInputType):
        write_bytes(self.h_prevouts, txi.prev_hash)
        write_uint32(self.h_prevouts, txi.prev_index)

    def get_prevouts_hash(self) -> bytes:
        return get_tx_hash(self.h_prevouts, True)

    def add_sequence(self, txi: TxInputType):
        write_uint32(self.h_sequence, txi.sequence)

    def get_sequence_hash(self) -> bytes:
        return get_tx_hash(self.h_sequence, True)

    def add_output(self, txo_bin: TxOutputBinType):
        write_tx_output(self.h_outputs, txo_bin)

    def get_outputs_hash(self) -> bytes:
        return get_tx_hash(self.h_outputs, True)

    def preimage(self, tx: SignTx, txi: TxInputType, script_code) -> bytes:

        h_preimage = HashWriter(sha256)

        write_uint32(h_preimage, tx.version)  # nVersion
        write_bytes(h_preimage, bytearray(self.get_prevouts_hash()))  # hashPrevouts
        write_bytes(h_preimage, bytearray(self.get_sequence_hash()))  # hashSequence
        write_bytes(h_preimage, txi.prev_hash)  # outpoint
        write_uint32(h_preimage, txi.prev_index)  # outpoint

        write_varint(h_preimage, len(script_code))  # scriptCode length
        write_bytes(h_preimage, bytearray(script_code))  # scriptCode

        write_uint64(h_preimage, txi.amount)  # amount
        write_uint32(h_preimage, txi.sequence)  # nSequence

        write_bytes(h_preimage, bytearray(self.get_outputs_hash()))  # hashOutputs
        write_uint32(h_preimage, tx.lock_time)  # nLockTime
        write_uint32(h_preimage, 0x00000001)  # nHashType  todo

        return get_tx_hash(h_preimage, True)

    # # returns outpoint, prevouts and sequence hashes
    # async def bip143_process_inputs(tx: SignTx):
    #
    #     h_prevouts = HashWriter(sha256)
    #     h_seq = HashWriter(sha256)
    #     tx_req = TxRequest()
    #     tx_req.details = TxRequestDetailsType()
    #     outpoint = bytearray()
    #
    #     # if hashType != ANYONE_CAN_PAY
    #     for i in range(tx.inputs_count):
    #         txi = await request_tx_input(tx_req, i)
    #         write_bytes(h_prevouts, txi.prev_hash)
    #         write_bytes(outpoint, txi.prev_hash)
    #         write_uint32(h_prevouts, txi.prev_index)
    #         write_uint32(outpoint, txi.prev_index)
    #         write_uint32(h_seq, txi.sequence)
    #
    #     return outpoint, get_tx_hash(h_prevouts, True), get_tx_hash(h_seq, True)
    #
    # # returns outputs hash
    # async def bip143_outputs(tx: SignTx, coin, root) -> bytes:
    #
    #     h_outputs = HashWriter(sha256)
    #     tx_req = TxRequest()
    #     tx_req.details = TxRequestDetailsType()
    #
    #     # if hashType != ANYONE_CAN_PAY
    #     for i in range(tx.outputs_count):
    #         txo = await request_tx_output(tx_req, i)
    #         txo_bin = TxOutputBinType()
    #         txo_bin.amount = txo.amount
    #         txo_bin.script_pubkey = output_derive_script(txo, coin, root)
    #         write_tx_output(h_outputs, txo_bin)
    #
    #     return get_tx_hash(h_outputs, True)
