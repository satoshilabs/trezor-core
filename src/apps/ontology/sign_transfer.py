from trezor import wire
from trezor.messages import OntologyAsset
from trezor.messages.OntologySignedTransfer import OntologySignedTransfer
from trezor.messages.OntologySignTransfer import OntologySignTransfer
from trezor.messages.OntologyTransaction import OntologyTransaction
from trezor.messages.OntologyTransfer import OntologyTransfer

from .layout import require_confirm_transfer_ong, require_confirm_transfer_ont
from .serialize import serialize_transfer
from .sign import sign


async def sign_transfer(ctx, msg: OntologySignTransfer):
    await _require_confirm(ctx, msg.transaction, msg.transfer)

    address_n = msg.address_n or ()
    [raw_data, payload] = serialize_transfer(msg.transaction, msg.transfer)
    signature = await sign(ctx, address_n, raw_data)

    return OntologySignedTransfer(signature=signature, payload=payload)


async def _require_confirm(
    ctx, transaction: OntologyTransaction, transfer: OntologyTransfer
):
    if transaction.type == 0xd1:
        if transfer.asset == OntologyAsset.ONT:
            return await require_confirm_transfer_ont(
                ctx, transfer.to_address, transfer.amount
            )
        if transfer.asset == OntologyAsset.ONG:
            return await require_confirm_transfer_ong(
                ctx, transfer.to_address, transfer.amount
            )

    raise wire.DataError("Invalid transaction type")
