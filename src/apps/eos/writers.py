from trezor.messages import EosAsset, EosAuthorization

from apps.common.writers import (
    write_bytes,
    write_uint8,
    write_uint16_le,
    write_uint32_le,
    write_uint64_le,
)


def write_auth(w: bytearray, auth: EosAuthorization) -> int:
    write_uint32_le(w, auth.threshold)
    write_variant32(w, len(auth.keys))
    for key in auth.keys:
        write_variant32(w, key.type)
        write_bytes(w, key.key)
        write_uint16_le(w, key.weight)

    write_variant32(w, len(auth.accounts))
    for account in auth.accounts:
        write_uint64_le(w, account.account.actor)
        write_uint64_le(w, account.account.permission)
        write_uint16_le(w, account.weight)

    write_variant32(w, len(auth.waits))
    for wait in auth.waits:
        write_uint32_le(w, wait.wait_sec)
        write_uint16_le(w, wait.weight)


def write_header(hasher: HashWriter, header: EosTxHeader):
    write_uint32_le(hasher, header.expiration)
    write_uint16_le(hasher, header.ref_block_num)
    write_uint32_le(hasher, header.ref_block_prefix)
    write_variant32(hasher, header.max_net_usage_words)
    write_uint8(hasher, header.max_cpu_usage_ms)
    write_variant32(hasher, header.delay_sec)


def write_action_transfer(hasher: HashWriter, msg: EosActionTransfer):
    w = bytearray()
    write_uint64_le(w, msg.sender)
    write_uint64_le(w, msg.receiver)
    write_asset(w, msg.quantity)
    write_variant32(w, len(msg.memo))
    write_bytes(w, msg.memo)
    write_variant32(hasher, len(w))
    write_bytes(hasher, w)


def write_action_buyram(hasher: HashWriter, msg: EosActionBuyRam):
    w = bytearray()
    write_uint64_le(w, msg.payer)
    write_uint64_le(w, msg.receiver)
    write_asset(w, msg.quantity)
    write_variant32(hasher, len(w))
    write_bytes(hasher, w)


def write_action_buyrambytes(hasher: HashWriter, msg: EosActionBuyRamBytes):
    w = bytearray()
    write_uint64_le(w, msg.payer)
    write_uint64_le(w, msg.receiver)
    write_uint32_le(w, msg.bytes)
    write_variant32(hasher, len(w))
    write_bytes(hasher, w)


def write_action_sellram(hasher: HashWriter, msg: EosActionSellRam):
    w = bytearray()
    write_uint64_le(w, msg.account)
    write_uint64_le(w, msg.bytes)
    write_variant32(hasher, len(w))
    write_bytes(hasher, w)


def write_action_delegate(hasher: HashWriter, msg: EosActionDelegate):
    w = bytearray()
    write_uint64_le(w, msg.sender)
    write_uint64_le(w, msg.receiver)
    write_asset(w, msg.net_quantity)
    write_asset(w, msg.cpu_quantity)
    write_uint8(w, 1 if msg.transfer else 0)
    write_variant32(hasher, len(w))
    write_bytes(hasher, w)


def write_action_undelegate(hasher: HashWriter, msg: EosActionUndelegate):
    w = bytearray()
    write_uint64_le(w, msg.sender)
    write_uint64_le(w, msg.receiver)
    write_asset(w, msg.net_quantity)
    write_asset(w, msg.cpu_quantity)
    write_variant32(hasher, len(w))
    write_bytes(hasher, w)


def write_action_refund(hasher: HashWriter, msg: EosActionRefund):
    w = bytearray()
    write_uint64_le(w, msg.owner)
    write_variant32(hasher, len(w))
    write_bytes(hasher, w)


def write_action_voteproducer(hasher: HashWriter, msg: EosActionVoteProducer):
    w = bytearray()
    write_uint64_le(w, msg.voter)
    write_uint64_le(w, msg.proxy)
    write_variant32(w, len(msg.producers))
    for producer in msg.producers:
        write_uint64_le(w, producer)
    write_variant32(hasher, len(w))
    write_bytes(hasher, w)


def write_action_updateauth(hasher: HashWriter, msg: EosActionUpdateAuth):
    w = bytearray()
    write_uint64_le(w, msg.account)
    write_uint64_le(w, msg.permission)
    write_uint64_le(w, msg.parent)
    write_auth(w, msg.auth)
    write_variant32(hasher, len(w))
    write_bytes(hasher, w)


def write_action_deleteauth(hasher: HashWriter, msg: EosActionDeleteAuth):
    w = bytearray()
    write_uint64_le(w, msg.account)
    write_uint64_le(w, msg.permission)
    write_variant32(hasher, len(w))
    write_bytes(hasher, w)


def write_action_linkauth(hasher: HashWriter, msg: EosActionLinkAuth):
    w = bytearray()
    write_uint64_le(w, msg.account)
    write_uint64_le(w, msg.code)
    write_uint64_le(w, msg.type)
    write_uint64_le(w, msg.requirement)
    write_variant32(hasher, len(w))
    write_bytes(hasher, w)


def write_action_unlinkauth(hasher: HashWriter, msg: EosActionLinkAuth):
    w = bytearray()
    write_uint64_le(w, msg.account)
    write_uint64_le(w, msg.code)
    write_uint64_le(w, msg.type)
    write_variant32(hasher, len(w))
    write_bytes(hasher, w)


def write_action_unknown(hasher: HashWriter, msg: EosActionUnknown):
    write_variant32(hasher, len(msg.data))
    write_bytes(hasher, msg.data)


def write_action_newaccount(hasher: HashWriter, msg: EosActionNewAccount):
    w = bytearray()
    write_uint64_le(w, msg.creator)
    write_uint64_le(w, msg.name)
    write_auth(w, msg.owner)
    write_auth(w, msg.active)
    write_variant32(hasher, len(w))
    write_bytes(hasher, w)


def write_action_common(hasher: HashWriter, msg: EosActionCommon):
    write_uint64_le(hasher, msg.account)
    write_uint64_le(hasher, msg.name)
    write_variant32(hasher, len(msg.authorization))
    for authorization in msg.authorization:
        write_uint64_le(hasher, authorization.actor)
        write_uint64_le(hasher, authorization.permission)


def write_asset(w: bytearray, asset: EosAsset) -> int:
    write_uint64_le(w, asset.amount)
    write_uint64_le(w, asset.symbol)


def write_variant32(w: bytearray, value: int) -> int:
    variant = bytearray()
    while True:
        b = value & 0x7F
        value >>= 7
        b |= (value > 0) << 7
        variant.append(b)

        if value == 0:
            break

    return write_bytes(w, bytes(variant))
