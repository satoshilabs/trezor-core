from trezor import wire
from trezor.messages.OntologyOntIdRegister import OntologyOntIdRegister
from trezor.messages.OntologySignedOntIdRegister import OntologySignedOntIdRegister
from trezor.messages.OntologySignOntIdRegister import OntologySignOntIdRegister
from trezor.messages.OntologyTransaction import OntologyTransaction

from .layout import require_confirm_ont_id_register
from .serialize import serialize_ont_id_register
from .sign import sign


async def sign_ont_id_register(ctx, msg: OntologySignOntIdRegister):
    await _require_confirm(ctx, msg.transaction, msg.ont_id_register)

    address_n = msg.address_n or ()
    [raw_data, payload] = serialize_ont_id_register(
        msg.transaction, msg.ont_id_register
    )

    signature = await sign(ctx, address_n, raw_data)

    return OntologySignedOntIdRegister(signature=signature, payload=payload)


async def _require_confirm(
    ctx, transaction: OntologyTransaction, register: OntologyOntIdRegister
):
    if transaction.type == 0xd1:
        return await require_confirm_ont_id_register(
            ctx, register.ont_id, register.public_key
        )

    raise wire.DataError("Invalid transaction type")
