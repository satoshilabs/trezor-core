from trezor.crypto.hashlib import sha256
from common import *

from apps.wallet.sign_tx.signing import *


async def bip143_preimage(tx: SignTx, root) -> bytes:

    # todo does this work for multiple inputs?
    coin = coins.by_name(tx.coin_name)
    h_preimage = HashWriter(sha256)
    tx_req = TxRequest()
    tx_req.details = TxRequestDetailsType()

    outpoint, prevouts, sequence = await bip143_process_inputs(tx)

    # if hashType != ANYONE_CAN_PAY
    for i in range(tx.inputs_count):
        txi = await request_tx_input(tx_req, i)
        write_uint32(h_preimage, tx.version)  # nVersion
        write_bytes(h_preimage, bytearray(prevouts))  # hashPrevouts
        write_bytes(h_preimage, bytearray(sequence))  # hashSequence
        write_bytes(h_preimage, outpoint)  # outpoint

        # todo: what to do with other types?
        scriptCode = output_derive_script(txi, coin, root)
        write_varint(h_preimage, len(scriptCode))  # scriptCode length
        write_bytes(h_preimage, bytearray(scriptCode))  # scriptCode

        write_uint64(h_preimage, txi.amount)  # amount
        write_uint32(h_preimage, txi.sequence)  # nSequence

        write_bytes(h_preimage, bytearray(await bip143_outputs(tx, coin, root)))  # hashOutputs
        write_uint32(h_preimage, tx.lock_time)  # nLockTime
        write_uint32(h_preimage, 0x00000001)  # nHashType  todo

        return get_tx_hash(h_preimage, True)


# returns outpoint, prevouts and sequence hashes
async def bip143_process_inputs(tx: SignTx):

    h_prevouts = HashWriter(sha256)
    h_seq = HashWriter(sha256)
    tx_req = TxRequest()
    tx_req.details = TxRequestDetailsType()
    outpoint = bytearray()

    # if hashType != ANYONE_CAN_PAY
    for i in range(tx.inputs_count):
        txi = await request_tx_input(tx_req, i)
        write_bytes(h_prevouts, txi.prev_hash)
        write_bytes(outpoint, txi.prev_hash)
        write_uint32(h_prevouts, txi.prev_index)
        write_uint32(outpoint, txi.prev_index)
        write_uint32(h_seq, txi.sequence)

    return outpoint, get_tx_hash(h_prevouts, True), get_tx_hash(h_seq, True)

# returns outputs hash
async def bip143_outputs(tx: SignTx, coin, root) -> bytes:

    h_outputs = HashWriter(sha256)
    tx_req = TxRequest()
    tx_req.details = TxRequestDetailsType()

    # if hashType != ANYONE_CAN_PAY
    for i in range(tx.outputs_count):
        txo = await request_tx_output(tx_req, i)
        txo_bin = TxOutputBinType()
        txo_bin.amount = txo.amount
        txo_bin.script_pubkey = output_derive_script(txo, coin, root)
        write_tx_output(h_outputs, txo_bin)

    return get_tx_hash(h_outputs, True)
