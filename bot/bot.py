from db import Users, Admin
from telebot.util import quick_markup, antiflood, extract_arguments
from dotenv import load_dotenv
import os
import telebot
import funcs
from time import sleep, time


GROUP_ID = -1002083631758


load_dotenv()

TOKEN  = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN, 'Markdown', disable_web_page_preview=True)

db_user = Users('users.db')
db_user.setup()

db_admin = Admin()
db_admin.setup()


@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    print(message.from_user.id)
    messager = message.chat.id
    if str(messager) == "7034272819" or str(messager) == "6219754372":
        send = bot.send_message(message.chat.id,"Enter message to broadcast")
        bot.register_next_step_handler(send,sendall)

    else:
        bot.reply_to(message, "You're not allowed to use this command")



def sendall(message):
    users = db_user.get_users()
    for chatid in users:
        try:
            msg = antiflood(bot.send_message, chatid, message.text)
        except Exception as e:
            print(e)

    bot.send_message(message.chat.id, "done")


@bot.message_handler(commands=['userno'])
def userno(message):
    print(message.from_user.id)
    messager = message.chat.id
    if str(messager) == "7034272819" or str(messager) == "6219754372":
        x = db_user.get_users()
        bot.reply_to(message,f"Total bot users: {len(x)}")
    else:
        bot.reply_to(message, "admin command")


def newlink():
    invite = bot.create_chat_invite_link(GROUP_ID,member_limit=1, expire_date=int(time())+10800)
    
    inv = invite.invite_link
    
    return inv


@bot.message_handler(commands=['start'])
def start(message):
    owner = message.chat.id
    name = message.chat.first_name
    db_user.add_user(owner)
    print(name)
    msg = f"""Welcome to *FLY Bot* {name}
 
Our Proof of Concept Bot for ButterFly AI, designed to showcase how our innovative connectionless technology enhances user experience while maintaining security. This bot offers two key features to demonstrate our approach:

*Wallet Trade & PnL History*

Get quick access to your wallet trade history and PnL (Profit and Loss) history through our Telegram bot. This feature demonstrates how users can view key wallet data effortlessly. While accessing wallet trade history typically does not require a direct wallet connection, we are showcasing this capability as part of our proof of concept, illustrating how easy it is to access important metrics without unnecessary wallet authorizations.

*Exclusive Access to Holders-Only Group*

We are demonstrating connectionless access to token-gated communities with this proof of concept. By holding a minimum of 0.05% of the total $FLY token supply, you gain exclusive access to our holders-only Telegram group—all without the need for traditional wallet connections. Instead of manually connecting your wallet, our approach verifies your token holdings seamlessly, ensuring secure and straightforward access for our loyal community members.

With this proof of concept, we aim to demonstrate the power and convenience of connectionless blockchain interactions, bringing a new level of simplicity and security to the user experience. Explore our bot and witness firsthand how ButterFly AI makes blockchain engagement more accessible and secure for everyone.
    """
    markup = quick_markup({
        'Wallet PnL Checker' : {'callback_data' : 'wallet'},
        'Exclusive Access Group' : {'callback_data' : 'exclusive'},
    },1)
    bot.send_message(owner, msg, reply_markup=markup)
    
    
@bot.message_handler(commands=['addadmin'])
def add_admin(message):
    owner = message.chat.id
    if str(owner) == "7034272819" or str(owner) == "6219754372":
        uid = int(extract_arguments(message.text))
        if uid:
           db_admin.add_user(uid) 
           bot.send_message(owner, "User successfully added to admin group")
        else:
            bot.send_message(owner, 'User id not found...')
    else:
        bot.send_message(owner, "You're not allowed to use this command")
        
        
@bot.message_handler(commands=['verify'])
def verify(message):
    owner = message.chat.id
    admin = db_admin.get_users()
    if owner in admin:
        uid = int(extract_arguments(message.text))
        if uid:
            y = newlink()
            print(y)
            bot.send_message(uid, f"You have been verified for access into exclusive group\n{y}", disable_web_page_preview=False)
        else:
            bot.send_message(owner, 'missing user uid\n use command as \n```/verify userid```')
    else:
        bot.send_message(owner, "you're not an admin")        
        
        
@bot.callback_query_handler(func= lambda call: True)
def call_back(call):
    owner = call.message.chat.id    
    
    if call.data == 'wallet':
        s = bot.send_message(owner, "Send Wallet address to perform analysis on")
        bot.register_next_step_handler(s, wallet_check)  
        
    elif call.data == 'pnl':
        wallet = db_user.get_wallet(owner)
        
        pnl = funcs.wallet_pnl(wallet)
        
        msg = f"""*Wallet PnL Analyzer*

*wallet*: `{wallet}`
                
*Total Trades*: {pnl['total_count_of_trades']}

*Total Profits USD*: ${round(float(pnl['total_realized_profit_usd']), 2)}

*Total Profit %*: {round(float(pnl['total_realized_profit_percentage']), 2)}%

*Total Buys | Sell*: {pnl['total_buys']} | {pnl['total_sells']}

*Total Volume*: ${round(float(pnl['total_trade_volume']), 2)}

*Volume Buy | Sell*: ${round(float(pnl['total_bought_volume_usd']), 2)} | $ {round(float(pnl['total_sold_volume_usd']), 2)}
                
        
    """ 
        markup = quick_markup({
            'Wallet PnL ' : {'callback_data' : 'pnl'}, 
            'Wallet PnL Breakdown ' : {'callback_data' : 'pnl_breakdown'},
            'Wallet Token Balances ' : {'callback_data' : 'balance'},
            'Wallet Tx history ' : {'callback_data' : 'history'},
            })
    
        bot.edit_message_text(msg, owner, call.message.message_id, reply_markup= markup)
        
    elif call.data == 'pnl_breakdown':
        wallet = db_user.get_wallet(owner)
        
        funcs.wallet_pnl_breakdown(wallet, owner)
        
        file = open(f'files/profits{owner}.txt', 'r')
        
        bot.send_document(owner, file, caption= f"Complete PnL Breakdown of trades made by `{wallet}`")
    
    
    elif call.data == 'history':
        wallet = db_user.get_wallet(owner)
        
        funcs.get_wallet_history(wallet, owner)
        
        file = open(f'files/history{owner}.txt', 'r')
        
        bot.send_document(owner, file, caption= f"Complete history of transactions made by `{wallet}`")

    
    elif call.data == 'balance':
        wallet = db_user.get_wallet(owner)
        msg = "Token Wallet Balances \n\n"
        balances = funcs.get_token_balances(wallet)
        for token in balances:
            name = token['name']
            balance = int(token['balance'])
            decimals = int(token['decimals'])
            addr = token['token_address']
            form = balance / (10**decimals)
            msg += f"[{name}](https://etherscan.io/token/{addr}): Balance: {form}\n"
        
        bot.send_message(owner, msg)
        
    elif call.data == 'exclusive':
        msg = """*Exclusive Access to Holders-Only Group*
        
We are demonstrating connectionless access to token-gated communities with this proof of concept. By holding a minimum of 0.25% (2.500.000 $FLY) of the total $FLY token supply, you gain exclusive access to our holders-only Telegram group—all without the need for traditional wallet connections. Instead of manually connecting your wallet, our approach verifies your token holdings seamlessly, ensuring secure and straightforward access for our loyal community members.

Please enter your wallet address where you hold minimum: 0.25% fly supply
"""
        
        s = bot.send_message(owner, msg)
        bot.register_next_step_handler(s, walleter)
        
    elif call.data == 'confend':
        s = bot.send_message(owner, 'Please send the transaction hash (COMPLETE ETHERSCAN LINK): ')
        bot.register_next_step_handler(s, conf)
        
        
def walleter(message):
    owner = message.chat.id
    wallet = str(message.text)
    if wallet.startswith('0x') and len(wallet) == 42:
        db_user.update_wallet(wallet, owner)
        msg = f"""To confirm token holdings, send 0.0001eth to this wallet address from the wallet address you entered 

Your wallet : *{wallet}*

Please send eth to below address and then click confirm once the transaction is confirmed on etherscan
`0x8e6c37ba15fb4a4013ef78554c40a7ed7eddf4c7` (tap to copy)   
        """
        markup = quick_markup({
            'Confirm ✅' : {'callback_data' : 'confend'},
            'Edit 📝' : {'callback_data' : 'exclusive'}
        })
        bot.send_message(owner, msg, reply_markup=markup)
    else:
        bot.send_message(owner, "Wallet address not valid.")

def conf(message):
    owner = message.chat.id
    tx_hash = message.text
    admins = db_admin.get_users()
    msgs = f"New wallet validation!!!\n\nUser: `{owner}`\n tx hash: {tx_hash}"
    for chatid in admins:
        try:
            msg = antiflood(bot.send_message, chatid, msgs)
        except Exception as e:
            print(e)
            
    bot.send_message(owner, "Verification under review...\nYou will receive a chat invite link if you passed verification.")
    
    
def wallet_check(message):
    owner = message.chat.id
    wallet = str(message.text)
    try:
        if wallet.startswith('0x'):
            db_user.update_wallet(wallet, owner)
        else:
            bot.send_message(owner, "Send a valid wallet address...")
        markup = quick_markup({
            'Wallet PnL ' : {'callback_data' : 'pnl'}, 
            'Wallet PnL Breakdown ' : {'callback_data' : 'pnl_breakdown'},
            'Wallet Token Balances ' : {'callback_data' : 'balance'},
            'Wallet Tx history ' : {'callback_data' : 'history'},
        })
        worth = funcs.get_wallet_worth(wallet)
        msg = f"""*Wallet Info*
        
*Total Bal*: ${round(float(worth['total_networth_usd']), 3)}

*Eth Bal*: {round(float(worth['chains'][0]['native_balance_formatted']),3)} ETH | usd: ${round(float(worth['chains'][0]['native_balance_usd']),3)}

*Token Bal. *: ${round(float(worth['chains'][0]['token_balance_usd']), 2)}

        """
        bot.send_message(owner, msg, reply_markup=markup)
    except Exception as e:
        print(e)


bot.infinity_polling()