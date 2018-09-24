"""Main wallet code for HackCoin.
"""

from blockchain import Blockchain, Transaction
from crypto import generate_keys, sign
from pyfiglet import Figlet
from utils import get_route, gen_uuid
from constants import WALLET_FILE, TXN_FILE

import os
import json
import jsonpickle

public = None
private = None
blockchain = None

def print_header():
    """Why not.
    """
    f = Figlet(font='slant')
    print f.renderText('HackCoin')

def load_or_create():
    """Load an existing wallet, or create a
    new one.
    """
    global public
    global private

    if os.path.exists(WALLET_FILE):
        # Load existing.
        with open(WALLET_FILE, 'r') as f:
            wallet_contents = f.read()
        wallet_obj = json.loads(wallet_contents)
        public = wallet_obj['public']
        private = wallet_obj['private']

        print "Loaded existing wallet from", WALLET_FILE
    else:
        # Create a new address and dump it.
        private, public = generate_keys()

        wallet_contents = json.dumps({
            'public': public,
            'private': private
        })

        with open(WALLET_FILE, 'w') as f:
            f.write(wallet_contents)
        print "Created new wallet in", WALLET_FILE
        
    print "Your wallet address is:", public

def load_blockchain():
    server_blockchain = get_route('blockchain', json=False)
    server_blockchain = server_blockchain.replace('hackcoin.core.', '')
    return jsonpickle.decode(server_blockchain)

def get_blockchain():
    """Loads the server blockchain state.
    """
    global blockchain

    blockchain = load_blockchain()

def get_balance(address):
    global blockchain

    get_blockchain()

    return blockchain.get_wallet_amount(address)

def balance(address):
    print "The balance is: " + str(get_balance(address)), "hackcoins."

def transaction(receiver, amount):
    global public
    global private
    global blockchain

    if get_balance(public) < amount:
        print "You don't have enough HackCoins."
        return

    # Build a new transaction.
    t = Transaction(
        id = gen_uuid(),
        owner = public,
        receiver = receiver,
        coins = amount,
        signature = None
    )

    # Sign it.
    t.signature = sign(t.comp(), private)

    # Place it in the miner queue to be mined.
    txns = []
    if os.path.exists(TXN_FILE):
        with open(TXN_FILE, 'r') as f:
            txns_json = f.read()
            txns = jsonpickle.decode(txns_json)
    
    txns.append(t)
    with open(TXN_FILE, 'w') as f:
        f.write(jsonpickle.encode(txns))

def start_repl():
    global public

    while True:
        command = raw_input("> ").split()
        if len(command) == 0:
            print "Type a valid command."
        elif command[0] == 'help' or command[0] == 'halp':
            print "Read README.md"
        elif command[0] == 'quit':
            break
        elif command[0] == 'balance':
            address = public
            if len(command) >= 2:
                address = command[1]
            balance(address)
        elif command[0] == 'pay':
            if len(command) < 3:
                print "Invalid syntax, it's pay <payee> <amount>"
            payee = command[1]
            amount = int(command[2])

            transaction(payee, amount)
        
if __name__ == "__main__":
    print_header()
    load_or_create()

    start_repl()