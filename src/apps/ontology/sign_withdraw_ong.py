from trezor import wire
from trezor.messages.OntologySignedWithdrawOng import OntologySignedWithdrawOng
from trezor.messages.OntologySignWithdrawOng import OntologySignWithdrawOng
from trezor.messages.OntologyTransaction import OntologyTransaction
from trezor.messages.OntologyWithdrawOng import OntologyWithdrawOng

from .layout import require_confirm_withdraw_ong
from .serialize import serialize_withdraw_ong
from .sign import sign


async def sign_withdraw_ong(ctx, msg: OntologySignWithdrawOng):
    await _require_confirm(ctx, msg.transaction, msg.withdraw_ong)

    address_n = msg.address_n or ()
    [raw_data, payload] = serialize_withdraw_ong(msg.transaction, msg.withdraw_ong)
    signature = await sign(ctx, address_n, raw_data)

    return OntologySignedWithdrawOng(signature=signature, payload=payload)


async def _require_confirm(
    ctx, transaction: OntologyTransaction, transfer: OntologyWithdrawOng
):
    if transaction.type == 0xd1:
        return await require_confirm_withdraw_ong(ctx, transfer.amount)

    raise wire.DataError("Invalid transaction type")
