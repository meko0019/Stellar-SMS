import re

from client.transactions.tasks import process_tx, create_tx
from client.transactions.utils import tx_pending, otp_required, check_otp

SEND_PATTERN = re.compile(r"^(send\s*)(\w+)(\s*\d+)(\s*\w*)$")


def sms_handler(message):
    body = message.get("Body").strip().lower()
    from_ = message.get("From")
    if tx_pending(from_):
        if body in ["y", "yes"]:
            otp = otp_required(from_)
            if otp:
                return "Incorrect password. Your transaction has been canceled."
            process_tx.delay(from_)
            return "Your transaction has been submitted."
        if check_otp(from_, body):
            process_tx.delay(from_)
            return "Your transaction has been submitted."
        return "Your transaction has been canceled."

    return sms_parser(from_, body)


def sms_parser(from_, sms):
    match = SEND_PATTERN.match(sms)
    if not match:
        return "Invalid transaction. Please try again."
    if len(match.group(2)) == 56:  # stellar address (public key)
        create_tx.delay(
            from_=from_,
            to=match.group(2),
            amount=match.group(3),
            currency=match.group(4),
        )
        return ""
    address = address_lookup(match.group(2))
    if address:
        create_tx.delay(
            from_=from_,
            to=address,
            amount=match.group(3),
            currency=match.group(4),
        )
        return ""
    return "Invalid address. Please try again."
    # TODO: handle federation addresses

def address_lookup(name):
    pass

