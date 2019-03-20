from apps.kin import consts, writers
from apps.kin.operations import layout, serialize


async def process_operation(ctx, w, op):
    if op.source_account:
        await layout.confirm_source_account(ctx, op.source_account)
    serialize.write_account(w, op.source_account)
    writers.write_uint32(w, consts.get_op_code(op))
    if isinstance(op, serialize.KinAccountMergeOp):
        await layout.confirm_account_merge_op(ctx, op)
        serialize.write_account_merge_op(w, op)
    elif isinstance(op, serialize.KinAllowTrustOp):
        await layout.confirm_allow_trust_op(ctx, op)
        serialize.write_allow_trust_op(w, op)
    elif isinstance(op, serialize.KinBumpSequenceOp):
        await layout.confirm_bump_sequence_op(ctx, op)
        serialize.write_bump_sequence_op(w, op)
    elif isinstance(op, serialize.KinChangeTrustOp):
        await layout.confirm_change_trust_op(ctx, op)
        serialize.write_change_trust_op(w, op)
    elif isinstance(op, serialize.KinCreateAccountOp):
        await layout.confirm_create_account_op(ctx, op)
        serialize.write_create_account_op(w, op)
    elif isinstance(op, serialize.KinCreatePassiveOfferOp):
        await layout.confirm_create_passive_offer_op(ctx, op)
        serialize.write_create_passive_offer_op(w, op)
    elif isinstance(op, serialize.KinManageDataOp):
        await layout.confirm_manage_data_op(ctx, op)
        serialize.write_manage_data_op(w, op)
    elif isinstance(op, serialize.KinManageOfferOp):
        await layout.confirm_manage_offer_op(ctx, op)
        serialize.write_manage_offer_op(w, op)
    elif isinstance(op, serialize.KinPathPaymentOp):
        await layout.confirm_path_payment_op(ctx, op)
        serialize.write_path_payment_op(w, op)
    elif isinstance(op, serialize.KinPaymentOp):
        await layout.confirm_payment_op(ctx, op)
        serialize.write_payment_op(w, op)
    elif isinstance(op, serialize.KinSetOptionsOp):
        await layout.confirm_set_options_op(ctx, op)
        serialize.write_set_options_op(w, op)
    else:
        raise ValueError("Unknown operation")
