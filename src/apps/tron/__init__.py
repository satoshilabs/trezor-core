from trezor import wire
from trezor.messages import MessageType


def boot():
    wire.add(MessageType.TronGetAddress, __name__, "get_address")
    wire.add(MessageType.TronSignTx, __name__, "sign_tx")
