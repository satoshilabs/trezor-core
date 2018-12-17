from trezor import wire
from trezor.messages import MessageType

from apps.common import HARDENED


def boot():
    ns = [["secp256k1", HARDENED | 44, HARDENED | 1397]]
    wire.add(MessageType.HyconGetAddress, __name__, "get_address", ns)
    wire.add(MessageType.HyconSignTx, __name__, "sign_tx", ns)
