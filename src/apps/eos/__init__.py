from trezor import wire
from trezor.messages import MessageType


def boot():
    wire.add(MessageType.EosGetPublicKey, __name__, "get_public_key")
    wire.add(MessageType.EosSignTx, __name__, "sign_tx")
