import ustruct

from apps.common.writers import (
    write_bytes,
    write_uint16_le,
    write_uint32_le,
    write_uint64_le,
    write_uint8
)

from trezor.messages.OnegramAsset import OnegramAsset
from trezor.messages.OnegramSignTx import OnegramSignTx
from trezor.messages.OnegramTxHeader import OnegramTxHeader


def write_common(w: bytearray, msg: OnegramSignTx):
    written = write_header(w, msg.header)
    written += write_uint8(w, 1)  # the number of operations
    return written


def write_header(w: bytearray, header: OnegramTxHeader):
    ref_block_num = header.head_block_number & 0xFFFF
    written = write_uint16_le(w, ref_block_num)

    ref_block_prefix = ustruct.unpack_from('<I', header.head_block_id, 4)[0]
    written += write_uint32_le(w, ref_block_prefix)

    written += write_uint32_le(w, header.expiration)
    return written


def write_transfer(w: bytearray, msg: OnegramSignTx):
    written = write_uint8(w, 0)  # 0 is the ID of transfer
    written += write_asset(w, msg.fee)
    written += write_asset_id(w, msg.source)
    written += write_asset_id(w, msg.destination)
    written += write_asset(w, msg.amount)

    # ignoring memo for now - setting it to 0x000000
    written += write_uint8(w, 0)
    written += write_uint8(w, 0)
    written += write_uint8(w, 0)
    return written


def write_varint(w: bytearray, val: int):
    data = b'' if val >= 0x80 else bytes([val])
    while val >= 0x80:
        data += bytes([(val & 0x7f) | 0x80])
        val >>= 7
        data += bytes([val])
    
    w += data
    return len(data)


def write_asset_id(w: bytearray, asset_str: str):
    asset_id = asset_str.split(".")[2]
    return write_varint(w, int(asset_id))


def write_asset(w: bytearray, asset: OnegramAsset):
    written = write_uint64_le(w, asset.amount)
    written += write_asset_id(w, asset.asset_id)

    return written
