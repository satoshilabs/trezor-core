from trezor import wire
from trezor.messages.OntologyOntIdAddAttributes import OntologyOntIdAddAttributes
from trezor.messages.OntologyTransaction import OntologyTransaction

from .layout import require_confirm_ont_id_add_attributes
from .serialize import serialize_ont_id_add_attributes
from .sign import sign

from trezor.messages.OntologySignedOntIdAddAttributes import (  # isort:skip
    OntologySignedOntIdAddAttributes
)
from trezor.messages.OntologySignOntIdAddAttributes import (  # isort:skip
    OntologySignOntIdAddAttributes
)


async def sign_ont_id_add_attributes(ctx, msg: OntologySignOntIdAddAttributes):
    await _require_confirm(ctx, msg.transaction, msg.ont_id_add_attributes)

    address_n = msg.address_n or ()
    [raw_data, payload] = serialize_ont_id_add_attributes(
        msg.transaction, msg.ont_id_add_attributes
    )
    signature = await sign(ctx, address_n, raw_data)

    return OntologySignedOntIdAddAttributes(signature=signature, payload=payload)


async def _require_confirm(
    ctx, transaction: OntologyTransaction, add: OntologyOntIdAddAttributes
):
    if transaction.type == 0xd1:
        return await require_confirm_ont_id_add_attributes(
            ctx, add.ont_id, add.public_key, add.ont_id_attributes
        )

    raise wire.DataError("Invalid transaction type")
