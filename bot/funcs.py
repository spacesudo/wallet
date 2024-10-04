from dotenv import load_dotenv
import os
import requests
from moralis import evm_api
import json

load_dotenv()

api_key = os.getenv('API_KEY')

def wallet_pnl(address: str):
    params = {
        "chain": "eth",
        "address": address
    }
    result = evm_api.wallets.get_wallet_profitability_summary(
        api_key=api_key,
        params=params,
    )
    return result


def get_wallet_history(wallet: str, uid: int):
    params = {
        "chain": "eth",
        "order": "DESC",
        "address": wallet
    }
    result = evm_api.wallets.get_wallet_history(
        api_key=api_key,
        params=params,
    )
    
    rslt = str(result)
    with open(f'files/history{uid}.txt', 'w') as f:
        f.write(rslt)
        f.close()


def get_token_balances(wallet: str):
    params = {
        "chain": "eth",
        "exclude_spam": True,
        "address": wallet
        
    }
    result = evm_api.token.get_wallet_token_balances(
        api_key=api_key,
        params=params,
    )
    
    return result[:10] if len(result) > 10 else result


def get_wallet_worth(wallet: str):
    params = {
        "exclude_spam": True,
        "exclude_unverified_contracts": True,
        "address": wallet
    }
    
    result = evm_api.wallets.get_wallet_net_worth(
        api_key=api_key,
        params=params,
    )
    return result 

def wallet_pnl_breakdown(walllet: str, uid):
    params = {
    "chain": "eth",
    "address": walllet
    }

    result = evm_api.wallets.get_wallet_profitability(
    api_key=api_key,
    params=params,
    )
    rslt = str(result)
    with open(f'files/profits{uid}.txt', 'w') as f:
        f.write(rslt)
        f.close()
        

if __name__ == '__main__':
    w = '0x5F67cf7A50F0A74172dF82946Aff24625967731c'
    print(get_wallet_worth(w))
