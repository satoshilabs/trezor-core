from trezor import ui
from trezor.messages import ButtonRequestType
from trezor.ui.text import Text
from trezor.utils import chunks

from apps.common.confirm import *


async def require_confirm_reveal(ctx, pk):
    text = Text("Confirm reveal", ui.ICON_SEND, icon_color=ui.GREEN)
    text.normal("Public Key:")
    text.mono(*split_address(pk))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_tx(ctx, to, value):
    text = Text("Confirm sending", ui.ICON_SEND, icon_color=ui.GREEN)
    text.bold(format_amount(value))
    text.normal("to")
    text.mono(*split_address(to))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_fee(ctx, value, fee):
    text = Text("Confirm transaction", ui.ICON_SEND, icon_color=ui.GREEN)
    text.bold(format_amount(value))
    text.normal("fee:")
    text.bold(format_amount(fee))
    await require_hold_to_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_origination(ctx, address):
    text = Text("Confirm origination", ui.ICON_SEND, icon_color=ui.ORANGE)
    text.normal("Originate address")
    text.mono(*split_address(address))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_origination_fee(ctx, address, fee):
    text = Text("Confirm origination", ui.ICON_SEND, icon_color=ui.ORANGE)
    text.bold("fee: " + format_amount(fee))
    text.mono(*split_address(address))
    await require_hold_to_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_delegation(ctx, source):
    text = Text("Confirm delegation", ui.ICON_SEND, icon_color=ui.BLUE)
    text.normal("Delegated address:")
    text.mono(*split_address(source))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_delegate(ctx, to, fee):
    text = Text("Confirm delegation", ui.ICON_SEND, icon_color=ui.BLUE)
    text.bold("fee: " + format_amount(fee))
    text.normal("to")
    text.mono(*split_address(to))
    await require_hold_to_confirm(ctx, text, ButtonRequestType.SignTx)


def split_address(address):
    return chunks(address, 18)


def format_amount(value):
    return "%s XTZ" % (int(value) / 1000000)
