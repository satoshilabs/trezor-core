from trezor import wire
from trezor.messages import MessageType


def boot():
    wire.add(MessageType.OnegramGetPublicKey, __name__, "get_public_key")
