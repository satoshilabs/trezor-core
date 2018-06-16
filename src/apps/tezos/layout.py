from apps.common.confirm import *
from trezor import ui
from trezor.utils import chunks
from trezor.messages import ButtonRequestType
from trezor.ui.text import Text


async def require_confirm_tx(ctx, to, value):
    content = Text('Confirm sending', ui.ICON_SEND,
                   ui.BOLD, format_amount(value),
                   ui.NORMAL, 'to',
                   ui.MONO, *split_address(to),
                   icon_color=ui.GREEN)
    return await require_confirm(ctx, content, ButtonRequestType.SignTx)


async def require_confirm_fee(ctx, value, fee):
    content = Text('Confirm transaction', ui.ICON_SEND,
                   ui.BOLD, format_amount(value),
                   ui.NORMAL, 'fee:',
                   ui.BOLD, format_amount(fee),
                   icon_color=ui.GREEN)
    await require_hold_to_confirm(ctx, content, ButtonRequestType.SignTx)


def split_address(address):
    return chunks(address, 17)


def format_amount(value):
    # TODO: check if value has to be divided by some number
    return '%s XTZ' % value
