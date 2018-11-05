from trezor.crypto.hashlib import sha256
from trezor.messages.EosTxActionRequest import EosTxActionRequest
from trezor.utils import HashWriter

from apps.eos import consts, helpers, updaters
from apps.eos.actions import layout


async def process_action(ctx, sha, action):
    name = helpers.eos_name_to_string(action.common.name)
    account = helpers.eos_name_to_string(action.common.account)

    if not check_action(action, name, account):
        raise ValueError("Unknown action")

    updaters.hashupdate_action_common(sha, action.common)
    if name == "buyram":
        await layout.confirm_action_buyram(ctx, action.buy_ram)
        updaters.hashupdate_action_buyram(sha, action.buy_ram)
    elif name == "buyrambytes":
        await layout.confirm_action_buyrambytes(ctx, action.buy_ram_bytes)
        updaters.hashupdate_action_buyrambytes(sha, action.buy_ram_bytes)
    elif name == "sellram":
        await layout.confirm_action_sellram(ctx, action.sell_ram)
        updaters.hashupdate_action_sellram(sha, action.sell_ram)
    elif name == "delegatebw":
        await layout.confirm_action_delegate(ctx, action.delegate)
        updaters.hashupdate_action_delegate(sha, action.delegate)
    elif name == "undelegatebw":
        await layout.confirm_action_undelegate(ctx, action.undelegate)
        updaters.hashupdate_action_undelegate(sha, action.undelegate)
    elif name == "refund":
        await layout.confirm_action_refund(ctx, action.refund)
        updaters.hashupdate_action_refund(sha, action.refund)
    elif name == "transfer":
        await layout.confirm_action_transfer(ctx, action.transfer)
        updaters.hashupdate_action_transfer(sha, action.transfer)
    elif name == "voteproducer":
        await layout.confirm_action_voteproducer(ctx, action.vote_producer)
        updaters.hashupdate_action_voteproducer(sha, action.vote_producer)
    elif name == "updateauth":
        await layout.confirm_action_updateauth(ctx, action.update_auth)
        updaters.hashupdate_action_updateauth(sha, action.update_auth)
    elif name == "deleteauth":
        await layout.confirm_action_deleteauth(ctx, action.delete_auth)
        updaters.hashupdate_action_deleteauth(sha, action.delete_auth)
    elif name == "linkauth":
        await layout.confirm_action_linkauth(ctx, action.link_auth)
        updaters.hashupdate_action_linkauth(sha, action.link_auth)
    elif name == "unlinkauth":
        await layout.confirm_action_unlinkauth(ctx, action.unlink_auth)
        updaters.hashupdate_action_unlinkauth(sha, action.unlink_auth)
    elif name == "newaccount":
        await layout.confirm_action_newaccount(ctx, action.new_account)
        updaters.hashupdate_action_newaccount(sha, action.new_account)
    else:
        await process_unknown_action(ctx, sha, action)


async def process_unknown_action(ctx, sha, action):
    checksum = HashWriter(sha256)
    checksum.extend(helpers.pack_variant32(action.unknown.data_size))
    checksum.extend(action.unknown.data_chunk)

    updaters.hashupdate_variant32(sha, action.unknown.data_size)
    updaters.hashupdate_bytes(sha, action.unknown.data_chunk)
    bytes_left = action.unknown.data_size - len(action.unknown.data_chunk)

    while bytes_left != 0:
        action = await ctx.call(
            EosTxActionRequest(data_size=bytes_left), *consts.action_wire_types
        )

        if action.unknown is None:
            raise ValueError("Bad response. Unknown struct expected.")

        checksum.extend(action.unknown.data_chunk)
        updaters.hashupdate_bytes(sha, action.unknown.data_chunk)

        bytes_left -= len(action.unknown.data_chunk)
        if bytes_left < 0:
            raise ValueError("Bad response. Buffer overflow.")

    await layout.confirm_action_unknown(ctx, action.common, checksum.get_digest())


def check_action(action, name, account):
    if account == "eosio":
        if (
            (name == "buyram" and action.buy_ram is not None)
            or (name == "buyrambytes" and action.buy_ram_bytes is not None)
            or (name == "sellram" and action.sell_ram is not None)
            or (name == "delegatebw" and action.delegate is not None)
            or (name == "undelegatebw" and action.undelegate is not None)
            or (name == "refund" and action.refund is not None)
            or (name == "voteproducer" and action.vote_producer is not None)
            or (name == "updateauth" and action.update_auth is not None)
            or (name == "deleteauth" and action.delete_auth is not None)
            or (name == "linkauth" and action.link_auth is not None)
            or (name == "unlinkauth" and action.unlink_auth is not None)
            or (name == "newaccount" and action.new_account is not None)
        ):
            return True

    elif name == "transfer" and action.transfer is not None:
        return True

    if action.unknown is not None:
        return True

    return False
