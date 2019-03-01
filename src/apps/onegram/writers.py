import struct


def write_varint(w: bytearray, val: int):
    data = b''
    while n >= 0x80:
        data += bytes([(n & 0x7f) | 0x80])
        n >>= 7
        data += bytes([n])
    
    w += data
    return len(data)


def write_asset_id(w: bytearray, asset_str: str):
    asset_id = asset_str.split(".")[2]
    return write_varint(w, asset.asset_id)


def write_asset(w: bytearray, asset: OnegramAsset):
    amount_bytes = struct.pack("<q", asset.amount)
    w += amount_bytes
    written += len(amount_bytes)
    written += write_asset_id(w, asset.asset_id)

    return written
