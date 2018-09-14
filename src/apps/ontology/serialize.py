from trezor.messages import OntologyAsset
from trezor.messages.OntologyOntIdAddAttributes import OntologyOntIdAddAttributes
from trezor.messages.OntologyOntIdAttribute import OntologyOntIdAttribute
from trezor.messages.OntologyOntIdRegister import OntologyOntIdRegister
from trezor.messages.OntologyTransaction import OntologyTransaction
from trezor.messages.OntologyTransfer import OntologyTransfer
from trezor.messages.OntologyTxAttribute import OntologyTxAttribute
from trezor.messages.OntologyWithdrawOng import OntologyWithdrawOng

from . import const as Const, writer
from .helpers import get_hex_from_address
from .sc.native_builder import ParamStruct, build_native_call


def serialize_tx(tx: OntologyTransaction, payload: bytes):
    """
    Serializes transaction with already serialized payload
    """
    ret = bytearray()

    writer.write_byte(ret, tx.version)
    writer.write_byte(ret, tx.type)
    writer.write_uint32(ret, tx.nonce)
    writer.write_uint64(ret, tx.gas_price)
    writer.write_uint64(ret, tx.gas_limit)

    payer = get_hex_from_address(tx.payer)
    writer.write_bytes(ret, payer)

    writer.write_bytes(ret, payload)

    attributes = tx.tx_attributes
    writer.write_varint(ret, len(attributes))

    if attributes is not None:
        for attribute in attributes:
            _serialize_tx_attribute(ret, attribute)

    return ret


def serialize_transfer(tx: OntologyTransaction, transfer: OntologyTransfer):
    """
    Serializes transaction with specified transfer as payload
    """
    payload = _serialize_transfer_payload(transfer)
    return [serialize_tx(tx, payload), payload]


def serialize_withdraw_ong(tx: OntologyTransaction, withdraw_ong: OntologyWithdrawOng):
    """
    Serializes transaction with specified withdraw Ong as payload
    """
    payload = _serialize_withdraw_ong_payload(withdraw_ong)
    return [serialize_tx(tx, payload), payload]


def serialize_ont_id_register(tx: OntologyTransaction, register: OntologyOntIdRegister):
    """
    Serializes transaction with specified ONT ID registration as payload
    """
    payload = _serialize_ont_id_register_payload(register)
    return [serialize_tx(tx, payload), payload]


def serialize_ont_id_add_attributes(
    tx: OntologyTransaction, add: OntologyOntIdAddAttributes
):
    """
    Serializes transaction with specified ONT ID attributes adding as payload
    """
    payload = _serialize_ont_id_add_attributes_payload(add)
    return [serialize_tx(tx, payload), payload]


def _serialize_tx_attribute(ret: bytearray, attribute: OntologyTxAttribute):
    writer.write_byte(ret, attribute.usage)

    if attribute.data is not None:
        writer.write_bytes_with_length(ret, attribute.data)


def _serialize_transfer_payload(transfer: OntologyTransfer):
    from_address = get_hex_from_address(transfer.from_address)
    to_address = get_hex_from_address(transfer.to_address)
    amount = transfer.amount
    contract = ""

    if transfer.asset == OntologyAsset.ONT:
        contract = Const.ONT_CONTRACT
    else:
        contract = Const.ONG_CONTRACT

    struct = ParamStruct([from_address, to_address, amount])
    native_call = build_native_call("transfer", [[struct]], contract)

    ret = bytearray()
    writer.write_bytes_with_length(ret, native_call)
    return bytes(ret)


def _serialize_withdraw_ong_payload(withdraw_ong: OntologyWithdrawOng):
    from_address = get_hex_from_address(withdraw_ong.from_address)
    to_address = get_hex_from_address(withdraw_ong.to_address)
    amount = withdraw_ong.amount

    struct = ParamStruct([from_address, Const.ONT_CONTRACT, to_address, amount])
    native_call = build_native_call("transferFrom", [struct], Const.ONG_CONTRACT)

    ret = bytearray()
    writer.write_bytes_with_length(ret, native_call)
    return bytes(ret)


def _serialize_ont_id_register_payload(register: OntologyOntIdRegister):
    ont_id = register.ont_id.encode("hex")

    struct = ParamStruct([ont_id, register.public_key])
    native_call = build_native_call(
        "regIDWithPublicKey", [struct], Const.ONTID_CONTRACT
    )

    ret = bytearray()
    writer.write_bytes_with_length(ret, native_call)
    return bytes(ret)


def _serialize_ont_id_add_attributes_payload(add: OntologyOntIdAddAttributes):
    ont_id = add.ont_id.encode("hex")
    attributes = add.ont_id_attributes

    arguments = [ont_id, len(attributes)]

    for attribute in attributes:
        _serialize_ont_id_attribute(arguments, attribute)

    arguments.append(add.public_key)

    struct = ParamStruct(arguments)
    native_call = build_native_call("addAttributes", [struct], Const.ONTID_CONTRACT)

    ret = bytearray()
    writer.write_bytes_with_length(ret, native_call)
    return bytes(ret)


def _serialize_ont_id_attribute(arguments: list, attribute: OntologyOntIdAttribute):
    arguments.append(attribute.key.encode("hex"))
    arguments.append(attribute.type.encode("hex"))
    arguments.append(attribute.value.encode("hex"))
