import random
import string

def generate_random_name():
    return "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(6)
    )

def generate_nonce():
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(30)
    )

from web3 import Web3
from eth_keys.exceptions import BadSignature
from eth_account.messages import encode_defunct
from django.core.exceptions import BadRequest
from hexbytes import HexBytes

alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/taZ9NZPvUjmxtpI5222ioiFbBUVFQxCt"
w3 = Web3(Web3.HTTPProvider(alchemy_url))


def verify_signature(address, signature, message):
    try:
        recovered_address = w3.eth.account.recover_message(encode_defunct(text=message), signature=(signature))
        if address == recovered_address:
            return True
        return False
    except BadSignature:
        raise BadRequest()


