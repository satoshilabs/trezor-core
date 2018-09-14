from ubinascii import unhexlify

from . import opcode
from .. import writer


def write_push_bytes(ret: bytearray, param: bytes):
    """
    Writes PUSH BYTES instruction
    """
    length = len(param)

    if length < opcode.PUSHBYTES75:
        writer.write_byte(ret, length)
    elif length < 0x100:
        writer.write_byte(ret, opcode.PUSHDATA1)
        writer.write_byte(ret, length)
    elif length < 0x10000:
        writer.write_byte(ret, opcode.PUSHDATA2)
        writer.write_uint16(ret, length)
    else:
        writer.write_byte(ret, opcode.PUSHDATA4)
        writer.write_uint32(ret, length)

    writer.write_bytes(ret, param)


def write_push_int(ret: bytearray, param: int):
    """
    Writes PUSH INT instruction
    """
    if param == -1:
        writer.write_byte(ret, opcode.PUSHM1)
    elif param == 0:
        writer.write_byte(ret, opcode.PUSH0)
    elif 0 < param < 16:
        num = opcode.PUSH1 - 1 + param
        writer.write_byte(ret, num)
    else:
        # number encoded as 8 bytes
        num = bytearray()
        writer.write_uint64(num, param)
        write_push_bytes(ret, bytes(num))


def write_push_bool(ret: bytearray, param: bool):
    """
    Writes PUSH BOOL instruction
    """
    if param:
        writer.write_byte(ret, opcode.PUSHT)
    else:
        writer.write_byte(ret, opcode.PUSHF)


def write_push_hexstr(ret: bytearray, param: str):
    """
    Writes PUSH BYTES instruction from hex string
    """
    write_push_bytes(ret, unhexlify(param))
