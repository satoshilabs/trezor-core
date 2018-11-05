from trezor.messages import (
    EosActionBuyRam,
    EosActionBuyRamBytes,
    EosActionCommon,
    EosActionDelegate,
    EosActionDeleteAuth,
    EosActionLinkAuth,
    EosActionNewAccount,
    EosActionRefund,
    EosActionSellRam,
    EosActionTransfer,
    EosActionUndelegate,
    EosActionUnknown,
    EosActionUpdateAuth,
    EosActionVoteProducer,
    EosAsset,
    EosTxHeader,
)
from trezor.utils import HashWriter

from apps.common.writers import (
    write_bytes,
    write_uint8,
    write_uint16_le,
    write_uint32_le,
    write_uint64_le,
)
from apps.eos.helpers import pack_variant32
from apps.eos.writers import write_asset, write_auth, write_variant32


def hashupdate_action_newaccount(hasher: HashWriter, msg: EosActionNewAccount):
    w = bytearray()
    write_uint64_le(w, msg.creator)
    write_uint64_le(w, msg.name)
    write_auth(w, msg.owner)
    write_auth(w, msg.active)

    hashupdate_variant32(hasher, len(w))
    hashupdate_bytes(hasher, w)


def hashupdate_action_buyram(hasher: HashWriter, msg: EosActionBuyRam):
    w = bytearray()
    write_uint64_le(w, msg.payer)
    write_uint64_le(w, msg.receiver)
    write_asset(w, msg.quantity)

    hashupdate_variant32(hasher, len(w))
    hashupdate_bytes(hasher, w)


def hashupdate_action_buyrambytes(hasher: HashWriter, msg: EosActionBuyRamBytes):
    w = bytearray()
    write_uint64_le(w, msg.payer)
    write_uint64_le(w, msg.receiver)
    write_uint32_le(w, msg.bytes)

    hashupdate_variant32(hasher, len(w))
    hashupdate_bytes(hasher, w)


def hashupdate_action_sellram(hasher: HashWriter, msg: EosActionSellRam):
    w = bytearray()
    write_uint64_le(w, msg.account)
    write_uint64_le(w, msg.bytes)

    hashupdate_variant32(hasher, len(w))
    hashupdate_bytes(hasher, w)


def hashupdate_action_delegate(hasher: HashWriter, msg: EosActionDelegate):
    w = bytearray()
    write_uint64_le(w, msg.sender)
    write_uint64_le(w, msg.receiver)
    write_asset(w, msg.stake_net_quantity)
    write_asset(w, msg.stake_cpu_quantity)
    write_uint8(w, 1 if msg.transfer else 0)

    hashupdate_variant32(hasher, len(w))
    hashupdate_bytes(hasher, w)


def hashupdate_action_undelegate(hasher: HashWriter, msg: EosActionUndelegate):
    w = bytearray()
    write_uint64_le(w, msg.sender)
    write_uint64_le(w, msg.receiver)
    write_asset(w, msg.unstake_net_quantity)
    write_asset(w, msg.unstake_cpu_quantity)

    hashupdate_variant32(hasher, len(w))
    hashupdate_bytes(hasher, w)


def hashupdate_action_refund(hasher: HashWriter, msg: EosActionRefund):
    w = bytearray()
    write_uint64_le(w, msg.owner)

    hashupdate_variant32(hasher, len(w))
    hashupdate_bytes(hasher, w)


def hashupdate_action_voteproducer(hasher: HashWriter, msg: EosActionVoteProducer):
    w = bytearray()
    write_uint64_le(w, msg.voter)
    write_uint64_le(w, msg.proxy)
    write_variant32(w, len(msg.producers))
    for producer in msg.producers:
        write_uint64_le(w, producer)

    hashupdate_variant32(hasher, len(w))
    hashupdate_bytes(hasher, w)


def hashupdate_action_transfer(hasher: HashWriter, msg: EosActionTransfer):
    w = bytearray()
    write_uint64_le(w, msg.sender)
    write_uint64_le(w, msg.receiver)
    write_asset(w, msg.quantity)

    write_variant32(w, len(msg.memo))
    write_bytes(w, msg.memo)

    hashupdate_variant32(hasher, len(w))
    hashupdate_bytes(hasher, w)


def hashupdate_action_updateauth(hasher: HashWriter, msg: EosActionUpdateAuth):
    w = bytearray()
    write_uint64_le(w, msg.account)
    write_uint64_le(w, msg.permission)
    write_uint64_le(w, msg.parent)
    write_auth(w, msg.auth)

    hashupdate_variant32(hasher, len(w))
    hashupdate_bytes(hasher, w)


def hashupdate_action_deleteauth(hasher: HashWriter, msg: EosActionDeleteAuth):
    w = bytearray()
    write_uint64_le(w, msg.account)
    write_uint64_le(w, msg.permission)

    hashupdate_variant32(hasher, len(w))
    hashupdate_bytes(hasher, w)


def hashupdate_action_linkauth(hasher: HashWriter, msg: EosActionLinkAuth):
    w = bytearray()
    write_uint64_le(w, msg.account)
    write_uint64_le(w, msg.code)
    write_uint64_le(w, msg.type)
    write_uint64_le(w, msg.requirement)

    hashupdate_variant32(hasher, len(w))
    hashupdate_bytes(hasher, w)


def hashupdate_action_unlinkauth(hasher: HashWriter, msg: EosActionLinkAuth):
    w = bytearray()
    write_uint64_le(w, msg.account)
    write_uint64_le(w, msg.code)
    write_uint64_le(w, msg.type)

    hashupdate_variant32(hasher, len(w))
    hashupdate_bytes(hasher, w)


def hashupdate_action_unknown(hasher: HashWriter, msg: EosActionUnknown):
    hashupdate_variant32(hasher, len(msg.data))
    hashupdate_bytes(hasher, msg.data)


def hashupdate_action_common(hasher: HashWriter, msg: EosActionCommon):
    hashupdate_uint64(hasher, msg.account)
    hashupdate_uint64(hasher, msg.name)
    hashupdate_variant32(hasher, len(msg.authorization))
    for authorization in msg.authorization:
        hashupdate_uint64(hasher, authorization.actor)
        hashupdate_uint64(hasher, authorization.permission)


def hashupdate_header(hasher: HashWriter, header: EosTxHeader):
    hashupdate_uint32(hasher, header.expiration)
    hashupdate_uint16(hasher, header.ref_block_num)
    hashupdate_uint32(hasher, header.ref_block_prefix)
    hashupdate_variant32(hasher, header.max_net_usage_words)
    hashupdate_uint8(hasher, header.max_cpu_usage_ms)
    hashupdate_variant32(hasher, header.delay_sec)


def hashupdate_bool(hasher: HashWriter, val: bool):
    w = bytearray()
    write_uint8(w, 1 if val else 0)
    hashupdate_bytes(hasher, w)


def hashupdate_uint64(hasher: HashWriter, val: int):
    w = bytearray()
    write_uint64_le(w, val)
    hashupdate_bytes(hasher, w)


def hashupdate_uint32(hasher: HashWriter, val: int):
    w = bytearray()
    write_uint32_le(w, val)
    hashupdate_bytes(hasher, w)


def hashupdate_uint16(hasher: HashWriter, val: int):
    w = bytearray()
    write_uint16_le(w, val)
    hashupdate_bytes(hasher, w)


def hashupdate_uint8(hasher: HashWriter, val: int):
    w = bytearray()
    write_uint8(w, val)
    hashupdate_bytes(hasher, w)


def hashupdate_variant32(hasher: HashWriter, val: int):
    packed = pack_variant32(val)
    hashupdate_bytes(hasher, packed)


def hashupdate_asset(hasher: HashWriter, asset: EosAsset):
    hashupdate_uint64(hasher, asset.amount)
    hashupdate_uint64(hasher, asset.symbol)


def hashupdate_bytes(hasher: HashWriter, data: bytearray):
    hasher.extend(data)
