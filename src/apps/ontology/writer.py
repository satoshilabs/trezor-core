def write_byte(w: bytearray, n: int):
    """
    Writes one byte (8bit)
    """
    w.append(n & 0xFF)


def write_uint16(w: bytearray, n: int):
    """
    Writes short (16bit)
    """
    w.append(n & 0xFF)
    w.append((n >> 8) & 0xFF)


def write_uint32(w: bytearray, n: int):
    """
    Writes int (32bit)
    """
    w.append(n & 0xFF)
    w.append((n >> 8) & 0xFF)
    w.append((n >> 16) & 0xFF)
    w.append((n >> 24) & 0xFF)


def write_uint64(w: bytearray, n: int):
    """
    Writes long (64bit)
    """
    w.append(n & 0xFF)
    w.append((n >> 8) & 0xFF)
    w.append((n >> 16) & 0xFF)
    w.append((n >> 24) & 0xFF)
    w.append((n >> 32) & 0xFF)
    w.append((n >> 40) & 0xFF)
    w.append((n >> 48) & 0xFF)
    w.append((n >> 56) & 0xFF)


def write_bool(w: bytearray, n: bool):
    """
    Writes boolean
    """
    if n:
        write_byte(w, 1)
    else:
        write_byte(w, 0)


def write_varint(w: bytearray, n: int):
    """
    Writes variable length integer
    """
    assert 0 <= n <= 0xFFFFFFFF

    if n < 0xFD:
        w.append(n & 0xFF)
    elif n <= 0xFFFF:
        w.append(0xFD)
        write_uint16(w, n)
    elif n <= 0xFFFFFFFF:
        w.append(0xFE)
        write_uint32(w, n)
    else:
        w.append(0xFF)
        write_uint64(w, n)


def write_bytes(w: bytearray, buf: bytes):
    """
    Writes arbitrary byte sequence
    """
    w.extend(buf)


def write_bytes_with_length(w: bytearray, buf: bytes):
    """
    Writes arbitrary byte sequence prepended with the length using variable length integer
    """
    write_varint(w, len(buf))
    write_bytes(w, buf)
