from trezor.messages import OnegramAsset, OnegramSignTx, OnegramTxHeader
from trezor.utils import HashWriter

from apps.common.writers import (
    write_uint8,
    write_uint16_le,
    write_uint32_le,
)
from apps.onegram.writers import write_asset, write_asset_id, write_varint


def update_common(hasher: HashWriter, msg: OnegramSignTx):
    update_bytes(hasher, bytearray(msg.chain_id))
    update_header(hasher, msg.header)
    update_uint8(hasher, 1)  # the number of operations


def update_header(hasher: HashWriter, header: OnegramTxHeader):
    update_uint16(hasher, header.ref_block_num)
    update_uint32(hasher, header.ref_block_prefix)
    update_uint32(hasher, header.expiration)


def update_asset_id(hasher: HashWriter, asset_str: str):
    w = bytearray()
    write_asset_id(w, asset_str)
    update_bytes(w)


def update_asset(hasher: HashWriter, asset: OngramAsset):
    w = bytearray()
    write_asset(w, asset)
    update_bytes(hasher, w)


def update_transfer(hasher: HashWriter, msg: OnegramSignTx):
    update_uint8(hasher, 0)  # 0 is the ID of transfer
    update_asset(hasher, msg.fee)
    update_asset_id(hasher, msg.source)
    update_asset_id(hasher, msg.destination)
    update_asset(hasher, msg.amount)
    
    # ignoring memo for now - setting it to 0x000000
    update_uint8(hasher, 0)
    update_uint8(hasher, 0)
    update_uint8(hasher, 0)


def update_uint32(hasher: HashWriter, val: int):
    w = bytearray()
    write_uint32_le(w, val)
    update_bytes(hasher, w)


def update_uint16(hasher: HashWriter, val: int):
    w = bytearray()
    write_uint16_le(w, val)
    update_bytes(hasher, w)


def update_uint8(hasher: HashWriter, val: int)
    w = bytearray()
    write_uint8(val)
    update_bytes(hasher, w)


def update_bytes(hasher: HashWriter, data: bytearray):
    hasher.extend(data)
