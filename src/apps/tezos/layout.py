from trezor import ui
from trezor.messages import ButtonRequestType
from trezor.ui.text import Text
from trezor.utils import chunks

from apps.common.confirm import *


async def require_confirm_tx(ctx, to, value):
    content = Text(
        "Confirm sending",
        ui.ICON_SEND,
        ui.BOLD,
        format_amount(value),
        ui.NORMAL,
        "to",
        ui.MONO,
        *split_address(to),
        icon_color=ui.GREEN
    )
    return await require_confirm(ctx, content, ButtonRequestType.SignTx)


async def require_confirm_fee(ctx, value, fee):
    content = Text(
        "Confirm transaction",
        ui.ICON_SEND,
        ui.BOLD,
        format_amount(value),
        ui.NORMAL,
        "fee:",
        ui.BOLD,
        format_amount(fee),
        icon_color=ui.GREEN,
    )
    await require_hold_to_confirm(ctx, content, ButtonRequestType.SignTx)


# TODO
async def require_confirm_delegation(ctx):
    content = Text(
        "Confirm origination", ui.ICON_SEND, ui.BOLD, "TODO", icon_color=ui.GREEN
    )
    await require_hold_to_confirm(ctx, content, ButtonRequestType.SignTx)


# TODO: check if it we want to show more info
async def require_confirm_delegation(ctx, to, fee):
    content = Text(
        "Confirm delegation",
        ui.ICON_SEND,
        ui.BOLD,
        "fee: " + format_amount(fee),
        ui.NORMAL,
        "to",
        ui.MONO,
        *split_address(to),
        icon_color=ui.GREEN
    )
    await require_hold_to_confirm(ctx, content, ButtonRequestType.SignTx)


def split_address(address):
    return chunks(address, 17)


def format_amount(value):
    # TODO: divide value
    return "%s XTZ" % value
