from trezor.messages import EosAsset, EosAuthorization

from apps.common.writers import (
    write_bytes,
    write_uint16_le,
    write_uint32_le,
    write_uint64_le,
)
from apps.eos.helpers import pack_variant32


def write_asset(w: bytearray, asset: EosAsset) -> int:
    written = write_uint64_le(w, asset.amount)
    written += write_uint64_le(w, asset.symbol)
    return written


def write_auth(w: bytearray, auth: EosAuthorization) -> int:
    written = write_uint32_le(w, auth.threshold)

    written += write_variant32(w, len(auth.keys))
    for key in auth.keys:
        written += write_bytes(w, pack_variant32(key.type))
        written += write_bytes(w, key.key)
        written += write_uint16_le(w, key.weight)

    written += write_variant32(w, len(auth.accounts))
    for account in auth.accounts:
        written += write_uint64_le(w, account.account.actor)
        written += write_uint64_le(w, account.account.permission)
        written += write_uint16_le(w, account.weight)

    written += write_variant32(w, len(auth.waits))
    for wait in auth.waits:
        written += write_uint32_le(w, wait.wait_sec)
        written += write_uint16_le(w, wait.weight)

    return written


def write_variant32(w: bytearray, value: int) -> int:
    value_variant32 = pack_variant32(value)
    return write_bytes(w, value_variant32)
