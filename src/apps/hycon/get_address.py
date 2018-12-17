from trezor.messages.HyconAddress import HyconAddress
from trezor.messages.HyconGetAddress import HyconGetAddress

from apps.hycon import helpers

from apps.common import paths
from apps.common.layout import address_n_to_str, show_address, show_qr


async def get_address(ctx, msg: HyconGetAddress, keychain):
    await paths.validate_path(ctx, helpers.validate_full_path, path=msg.address_n)

    node = keychain.derive(msg.address_n)
    pubkey = node.public_key()
    addr = helpers.address_from_public_key(pubkey)
    address = helpers.address_to_string(addr)
    
    if msg.show_display:
        desc = address_n_to_str(msg.address_n)
        while True:
            if await show_address(ctx, address, desc=desc):
                break
            if await show_qr(ctx, address.upper(), desc=desc):
                break

    return HyconAddress(address=address)
