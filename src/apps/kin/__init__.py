from trezor import wire
from trezor.messages import MessageType

from apps.common import HARDENED


def boot():
    ns = [["ed25519", HARDENED | 44, HARDENED | 2017]]
    wire.add(MessageType.KinGetAddress, __name__, "get_address", ns)
    wire.add(MessageType.KinSignTx, __name__, "sign_tx", ns)
