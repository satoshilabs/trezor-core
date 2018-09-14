from trezor import wire
from trezor.messages import MessageType


def boot():
    wire.add(MessageType.OntologyGetPublicKey, __name__, "get_public_key")
    wire.add(MessageType.OntologyGetAddress, __name__, "get_address")
    wire.add(MessageType.OntologySignTransfer, __name__, "sign_transfer")
    wire.add(MessageType.OntologySignWithdrawOng, __name__, "sign_withdraw_ong")
    wire.add(MessageType.OntologySignOntIdRegister, __name__, "sign_ont_id_register")
    wire.add(
        MessageType.OntologySignOntIdAddAttributes,
        __name__,
        "sign_ont_id_add_attributes",
    )
