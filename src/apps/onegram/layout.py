from micropython import const

from trezor import ui
from trezor.ui.text import Text
from trezor.utils import format_amount
from trezor.messages import ButtonRequestType

from apps.common.confirm import require_confirm, require_hold_to_confirm


async def require_get_public_key(ctx, public_key):
    text = Text("Confirm public key", ui.ICON_RECEIVE, icon_color=ui.GREEN)
    text.normal(public_key)
    return await require_confirm(ctx, text, code=ButtonRequestType.PublicKey)


async def require_confirm_tx(ctx, source, destination, value):
    text = Text("Confirm sending", ui.ICON_SEND, icon_color=ui.GREEN)
    text.bold(format_onegram_amount(value))
    text.mono("from " + source)
    text.mono("to " + destination)
    return await require_confirm(ctx, text, code=ButtonRequestType.SignTx)


async def require_confirm_fee(ctx, value, fee):
    text = Text("Confirm transaction", ui.ICON_SEND, icon_color=ui.GREEN)
    text.normal("Amount:")
    text.bold(format_onegram_amount(value))
    text.normal("Fee:")
    text.bold(format_onegram_amount(fee))
    await require_hold_to_confirm(ctx, text, ButtonRequestType.SignTx)


def format_onegram_amount(value):
    formatted_value = format_amount(value, const(6))
    return formatted_value + " OGC"
