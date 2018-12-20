from trezor import ui
from trezor.ui.text import Text
from trezor.messages import ButtonRequestType

from apps.common.confirm import require_confirm


async def require_get_public_key(ctx, public_key):
    text = Text("Confirm public key", ui.ICON_RECEIVE, icon_color=ui.GREEN)
    text.normal(public_key)
    return await require_confirm(ctx, text, code=ButtonRequestType.PublicKey)