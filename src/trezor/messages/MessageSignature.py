# Automatically generated by pb2py
# fmt: off
import protobuf as p


class MessageSignature(p.MessageType):
    MESSAGE_WIRE_TYPE = 40
    FIELDS = {
        1: ('address', p.UnicodeType, 0),
        2: ('signature', p.BytesType, 0),
    }

    def __init__(
        self,
        address: str = None,
        signature: bytes = None,
    ) -> None:
        self.address = address
        self.signature = signature
