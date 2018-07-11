from trezor import ui
from trezor.messages import ButtonRequestType
from trezor.ui.text import Text
from trezor.utils import chunks

from .helpers import get_vote_tx_text

from apps.common.confirm import require_confirm, require_hold_to_confirm
from apps.wallet.get_public_key import _show_pubkey


async def require_confirm_tx(ctx, to, value):
    text = Text("Confirm sending", ui.ICON_SEND, icon_color=ui.GREEN)
    text.bold(format_amount(value))
    text.normal("to")
    text.mono(*split_address(to))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_delegate_registration(ctx, delegate_name):
    text = Text("Confirm transaction", ui.ICON_SEND, icon_color=ui.GREEN)
    text.normal("Do you really want to")
    text.normal("register a delegate?")
    text.bold(*chunks(delegate_name, 20))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_vote_tx(ctx, votes):
    text = Text("Confirm transaction", ui.ICON_SEND, icon_color=ui.GREEN)
    text.normal(*get_vote_tx_text(votes))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_public_key(ctx, public_key):
    return await _show_pubkey(ctx, public_key)


async def require_confirm_multisig(ctx, multisignature):
    text = Text("Confirm transaction", ui.ICON_SEND, icon_color=ui.GREEN)
    text.normal("Keys group length: %s" % len(multisignature.keys_group))
    text.normal("Life time: %s" % multisignature.life_time)
    text.normal("Min: %s" % multisignature.min)
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_fee(ctx, value, fee):
    text = Text("Confirm transaction", ui.ICON_SEND, icon_color=ui.GREEN)
    text.bold(format_amount(value))
    text.normal("fee:")
    text.bold(format_amount(fee))
    await require_hold_to_confirm(ctx, text, ButtonRequestType.ConfirmOutput)


def format_amount(value):
    return "%s LSK" % (int(value) / 100000000)


def split_address(address):
    return chunks(address, 16)
