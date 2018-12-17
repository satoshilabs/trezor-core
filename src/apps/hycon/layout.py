from trezor import ui
from trezor.messages import ButtonRequestType
from trezor.ui.text import Text
from trezor.utils import format_amount

from apps.common.confirm import require_confirm, require_hold_to_confirm
from apps.common.layout import split_address


async def require_confirm_fee(ctx, fee):
    text = Text("Confirm fee", ui.ICON_SEND, icon_color=ui.GREEN)
    text.normal("Transaction fee:")
    text.bold(fee + " HYC")
    await require_confirm(ctx, text, ButtonRequestType.ConfirmOutput)


async def require_confirm_destination_tag(ctx, tag):
    text = Text("Confirm tag", ui.ICON_SEND, icon_color=ui.GREEN)
    text.normal("Destination tag:")
    text.bold(str(tag))
    await require_confirm(ctx, text, ButtonRequestType.ConfirmOutput)


async def require_confirm_tx(ctx, to, value):

    text = Text("Confirm sending", ui.ICON_SEND, icon_color=ui.GREEN)
    text.bold(value + " HYC")
    text.normal("to")
    text.mono(to)
    return await require_hold_to_confirm(ctx, text, ButtonRequestType.SignTx)
