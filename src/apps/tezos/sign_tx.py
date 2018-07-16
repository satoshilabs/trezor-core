import ustruct

from trezor import wire
from trezor.crypto import hashlib
from trezor.crypto.curve import ed25519
from trezor.messages import TezosContractType, TezosOperationType
from trezor.messages.TezosSignedTx import TezosSignedTx

from apps.common import seed
from apps.tezos.helpers import (
    b58cencode,
    get_address_prefix,
    get_curve_module,
    get_curve_name,
    get_sig_prefix,
)
from apps.tezos.layout import *


async def tezos_sign_tx(ctx, msg):
    address_n = msg.address_n or ()
    curve = msg.curve or 0
    operation_type = msg.operation.tag

    node = await seed.derive_node(ctx, address_n, get_curve_name(curve))

    source = _get_address_from_contract(msg.operation.source)

    if operation_type == TezosOperationType.Transaction:
        to = _get_address_from_contract(msg.transaction.destination)
        await require_confirm_tx(ctx, to, msg.transaction.amount)
        await require_confirm_fee(ctx, msg.transaction.amount, msg.operation.fee)

    elif operation_type == TezosOperationType.Origination:
        await require_confirm_origination(ctx, source)
        await require_confirm_originate(ctx, source, msg.operation.fee)

    elif operation_type == TezosOperationType.Delegation:
        to = _get_address_by_tag(msg.delegation.delegate)
        await require_confirm_delegation(ctx, source)
        await require_confirm_delegate(ctx, to, msg.operation.fee)

    else:
        raise wire.DataError("Invalid operation type")

    opbytes = _get_operation_bytes(msg)

    watermark = bytes([3])
    wm_opbytes = watermark + opbytes
    wm_opbytes_hash = hashlib.blake2b(wm_opbytes, outlen=32).digest()

    curve_module = get_curve_module(curve)
    signature = curve_module.sign(node.private_key(), wm_opbytes_hash)

    sig_op_contents = opbytes + signature
    sig_op_contents_hash = hashlib.blake2b(sig_op_contents, outlen=32).digest()
    ophash = b58cencode(sig_op_contents_hash, prefix="o")

    sig_prefixed = b58cencode(signature, prefix=get_sig_prefix(curve))

    return TezosSignedTx(
        signature=sig_prefixed, sig_op_contents=sig_op_contents, operation_hash=ophash
    )


def _get_address_by_tag(address_hash):
    tag = int(address_hash[0])
    return b58cencode(address_hash[1:], prefix=get_address_prefix(tag))


def _get_address_from_contract(address):
    if address.tag == TezosContractType.Implicit:
        return _get_address_by_tag(address.hash)

    elif address.tag == TezosContractType.Originated:
        return b58cencode(address.hash[:-1], prefix="KT1")

    raise wire.DataError("Invalid contract type")


def _get_operation_bytes(msg):
    result = msg.operation.branch

    # common part
    result += ustruct.pack("<b", msg.operation.tag)
    result += _encode_contract_id(msg.operation.source)
    result += _encode_zarith(msg.operation.fee)
    result += _encode_zarith(msg.operation.counter)
    result += _encode_zarith(msg.operation.gas_limit)
    result += _encode_zarith(msg.operation.storage_limit)

    if msg.transaction is not None:
        # transaction part
        result += _encode_zarith(msg.transaction.amount)
        result += _encode_contract_id(msg.transaction.destination)
        result += _encode_data_with_bool_prefix(msg.transaction.parameters)
    elif msg.origination is not None:
        # origination part
        result += msg.origination.manager_pubkey
        result += _encode_zarith(msg.origination.balance)
        result += _encode_bool(msg.origination.spendable)
        result += _encode_bool(msg.origination.delegatable)
        result += _encode_data_with_bool_prefix(msg.origination.delegate)
        result += _encode_data_with_bool_prefix(msg.origination.script)
    elif msg.delegation is not None:
        # delegation part
        result += _encode_data_with_bool_prefix(msg.delegation.delegate)

    else:
        raise wire.DataError("Operation data not found")

    return bytes(result)


def _encode_contract_id(contract_id):
    return ustruct.pack("<b", contract_id.tag) + contract_id.hash


def _encode_bool(boolean):
    return ustruct.pack("<b", 255) if boolean else ustruct.pack("<b", 0)


def _encode_data_with_bool_prefix(data):
    return _encode_bool(True) + data if data is not None else _encode_bool(False)


def _encode_zarith(num):
    result = bytes()

    while True:
        byte = num & 127
        num = num >> 7

        if num == 0:
            result += ustruct.pack("<b", byte)
            break

        result += ustruct.pack("<b", 128 | byte)

    return result
