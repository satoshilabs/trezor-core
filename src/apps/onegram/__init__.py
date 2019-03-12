from trezor import wire
from trezor.messages import MessageType

from apps.common import HARDENED


def boot():
    ns = [["secp256k1", HARDENED | 48, HARDENED | 10]]
    wire.add(MessageType.OnegramGetPublicKey, __name__, "get_public_key", ns)
    wire.add(MessageType.OnegramSignTx, __name__, "sign_tx", ns)
