from trezor import ui, wire
from trezor.crypto import hmac
from trezor.crypto.aes import AES_CBC_Decrypt, AES_CBC_Encrypt
from trezor.crypto.hashlib import sha512
from trezor.messages.CipheredKeyValue import CipheredKeyValue
from trezor.ui.text import Text, TEXT_MARGIN_LEFT
from trezor.utils import split_words
from apps.common import seed
from apps.common.confirm import require_confirm


async def cipher_key_value(ctx, msg):
    if len(msg.value) % 16 > 0:
        raise wire.DataError('Value length must be a multiple of 16')

    encrypt = msg.encrypt
    decrypt = not msg.encrypt
    if (encrypt and msg.ask_on_encrypt) or (decrypt and msg.ask_on_decrypt):
        if encrypt:
            title = 'Encrypt value'
        else:
            title = 'Decrypt value'
        lines = split_words(msg.key, ui.WIDTH - 2 * TEXT_MARGIN_LEFT, metric=lambda x: ui.display.text_width(x, ui.NORMAL))
        await require_confirm(ctx, Text(title, ui.ICON_DEFAULT, max_lines=5, *lines))

    node = await seed.derive_node(ctx, msg.address_n)
    value = compute_cipher_key_value(msg, node.private_key())
    return CipheredKeyValue(value=value)


def compute_cipher_key_value(msg, seckey: bytes) -> bytes:
    data = msg.key
    data += 'E1' if msg.ask_on_encrypt else 'E0'
    data += 'D1' if msg.ask_on_decrypt else 'D0'
    data = hmac.new(seckey, data, sha512).digest()
    key = data[:32]
    if msg.iv and len(msg.iv) == 16:
        iv = msg.iv
    else:
        iv = data[32:48]

    if msg.encrypt:
        aes = AES_CBC_Encrypt(key=key, iv=iv)
    else:
        aes = AES_CBC_Decrypt(key=key, iv=iv)

    return aes.update(msg.value)
