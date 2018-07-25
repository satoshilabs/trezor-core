from ubinascii import hexlify

from trezor import log, wire
from trezor.crypto import bip32
from trezor.messages.CardanoPublicKey import CardanoPublicKey
from trezor.messages.HDNodeType import HDNodeType

from .address import (
    _break_address_n_to_lines,
    _derive_hd_passphrase,
    derive_address_and_node,
)
from .ui import show_swipable_with_confirmation

from apps.common import seed, storage


async def cardano_get_public_key(ctx, msg):
    mnemonic = storage.get_mnemonic()
    root_node = bip32.from_mnemonic_cardano(mnemonic)

    try:
        key = _get_public_key(root_node, msg.address_n)
    except ValueError as e:
        if __debug__:
            log.exception(__name__, e)
        raise wire.ProcessError("Deriving public key failed")
    mnemonic = None
    root_node = None

    lines = ["For BIP32 path: ", ""]
    lines.extend(_break_address_n_to_lines(msg.address_n))
    if not await show_swipable_with_confirmation(ctx, lines, "Export xpub key"):
        raise wire.ActionCancelled("Exporting cancelled")

    return key


def _get_public_key(root_node, derivation_path: list):
    _, node = derive_address_and_node(root_node, derivation_path)

    public_key = hexlify(seed.remove_ed25519_prefix(node.public_key())).decode("utf8")
    chain_code = hexlify(node.chain_code()).decode("utf8")
    xpub_key = public_key + chain_code
    root_hd_passphrase = hexlify(_derive_hd_passphrase(root_node)).decode("utf8")

    node_type = HDNodeType(
        depth=node.depth(),
        child_num=node.child_num(),
        fingerprint=node.fingerprint(),
        chain_code=node.chain_code(),
        public_key=seed.remove_ed25519_prefix(node.public_key()),
    )

    return CardanoPublicKey(
        node=node_type, xpub=xpub_key, root_hd_passphrase=root_hd_passphrase
    )
