from .models import User
from django.contrib.auth import authenticate, hashers #, get_user_model

def get_and_authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password.")
    return user

def create_user_account(email, password, username, **extra_fields):
    user = User.objects.create_user(email=email, username=username, 
                                    password=password, wallet_address=username, **extra_fields)
    return user

# # web3 helper 

# from web3 import Web3
# from hexbytes import HexBytes
# from eth_account.messages import encode_defunct
# w3 = Web3(Web3.HTTPProvider(""))
# mesage= encode_defunct(text="6875972781")
# address = w3.eth.account.recover_message(mesage,signature=HexBytes("0x0293cc0d4eb416ca95349b7e63dc9d1c9a7aab4865b5cd6d6f2c36fb1dce12d34a05039aedf0bc64931a439def451bcf313abbcc72e9172f7fd51ecca30b41dd1b"))
# print(address)
