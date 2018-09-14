from micropython import const
from ubinascii import hexlify

from trezor import ui
from trezor.messages import ButtonRequestType, MessageType
from trezor.messages.ButtonRequest import ButtonRequest
from trezor.ui.confirm import CONFIRMED, ConfirmDialog
from trezor.ui.scroll import Scrollpage, animate_swipe, paginate
from trezor.ui.text import Text
from trezor.utils import chunks

from apps.common.confirm import require_confirm


async def require_confirm_transfer_ont(ctx, dest, value):
    text = Text("Confirm sending", ui.ICON_SEND, icon_color=ui.GREEN)
    text.bold(format_amount_ont(value))
    text.mono(*split_address("To: " + dest))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_transfer_ong(ctx, dest, value):
    text = Text("Confirm sending", ui.ICON_SEND, icon_color=ui.GREEN)
    text.bold(format_amount_ong(value))
    text.mono(*split_address("To: " + dest))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_withdraw_ong(ctx, value):
    text = Text("Confirm withdraw of ", ui.ICON_SEND, icon_color=ui.GREEN)
    text.bold(format_amount_ong(value))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_ont_id_register(ctx, ont_id, public_key):
    title = "Confirm registering "
    key = hexlify(public_key).decode() + " "
    content = split_str(ont_id) + ["", "with public key "] + split_str(key)

    return await show_swipable_with_confirmation(ctx, content, title)


async def require_confirm_ont_id_add_attributes(ctx, ont_id, public_key, attributes):
    title = "Confirm attributes "
    key = hexlify(public_key).decode() + ": "
    content = split_str("for " + ont_id) + ["", "with public key "] + split_str(key)

    for attribute in attributes:
        content += split_str("Name: " + attribute.key)
        content += split_str("Type: " + attribute.type)
        content += split_str("Value: " + attribute.value)
        content.append("")

    return await show_swipable_with_confirmation(ctx, content, title)


def format_amount_ont(value):
    return "%s ONT" % (int(value))


def format_amount_ong(value):
    return "%s ONG" % (int(value) / 1000000000)


def split_address(address):
    return chunks(address, 16)


def split_str(text: str):
    return list(chunks(text, 16))


async def show_swipable_with_confirmation(ctx, content, title: str):
    first_page = const(0)
    lines_per_page = const(5)

    if isinstance(content, (list, tuple)):
        lines = content
    else:
        lines = list(chunks(content, 17))
    pages = list(chunks(lines, lines_per_page))

    await ctx.call(ButtonRequest(code=ButtonRequestType.SignTx), MessageType.ButtonAck)

    paginator = paginate(show_text_page, len(pages), first_page, pages, title)
    return await ctx.wait(paginator) == CONFIRMED


@ui.layout
async def show_text_page(page: int, page_count: int, pages: list, title: str):
    if page_count == 1:
        page = 0

    lines = pages[page]
    content = Text(title, ui.ICON_DEFAULT, icon_color=ui.GREEN)
    content.mono(*lines)

    content = Scrollpage(content, page, page_count)

    if page + 1 >= page_count:
        return await ConfirmDialog(content)

    content.render()
    await animate_swipe()
