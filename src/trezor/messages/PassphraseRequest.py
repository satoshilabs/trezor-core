# Automatically generated by pb2py
# fmt: off
import protobuf as p


class PassphraseRequest(p.MessageType):
    MESSAGE_WIRE_TYPE = 41
    FIELDS = {
        1: ('on_device', p.BoolType, 0),
    }

    def __init__(
        self,
        on_device: bool = None,
    ) -> None:
        self.on_device = on_device
