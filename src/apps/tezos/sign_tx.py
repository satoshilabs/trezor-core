import ustruct

from trezor import wire
from trezor.crypto import hashlib
from trezor.crypto.curve import ed25519
from trezor.messages import TezosContractType
from trezor.messages.TezosSignedTx import TezosSignedTx

from apps.common import seed
from apps.tezos.helpers import TEZOS_CURVES, b58cencode
from apps.tezos.layout import *


async def tezos_sign_tx(ctx, msg):
    address_n = msg.address_n or ()
    node = await seed.derive_node(ctx, address_n, "ed25519")

    # TODO: check if signing differs according to public_key_hash in source

    # operation_bytes = msg.operation_bytes
    # operation_hashed_bytes = hashlib.blake2b(operation_bytes, outlen=32).digest()
    # signature = ed25519.sign(node.private_key(), operation_hashed_bytes)

    # sig_op_contents = operation_bytes + signature
    # sig_op_contents_blaked = hashlib.blake2b(sig_op_contents, outlen=32).digest()
    # operation_hash = b58cencode(sig_op_contents_blaked, prefix='o')

    to = _get_address_by_type(msg.transaction.destination)

    # print(list(_get_operation_bytes(msg)))

    # TODO: raise invalid operation type if not supported

    await require_confirm_delegation(ctx, to, msg.operation.fee)
    # TODO: show layout according to OperationType
    await require_confirm_tx(ctx, to, msg.transaction.amount)
    await require_confirm_fee(ctx, msg.transaction.amount, msg.operation.fee)

    return TezosSignedTx(
        signature=bytes([1, 2, 3]),
        sig_op_contents=bytes([1, 2, 3]),
        operation_hash="testhash",
    )


def _get_address_by_type(address):
    if address.tag == TezosContractType.Implicit:
        # TODO: check if the prefix differs according to hash tag
        return b58cencode(address.hash[1:], prefix="tz1")

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
        raise wire.DataError("Invalid operation type")

    return result


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
