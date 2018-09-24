from blockchain import Block, Transaction, get_genisis
from crypto import sign
from wallet import load_blockchain
from constants import WALLET_FILE, TXN_FILE, REWARD
from utils import gen_uuid, get_route
from pyfiglet import Figlet

import datetime
import json
import os
import shutil
import jsonpickle

public = None
private = None
blockchain = None

def print_header():
    """Why not.
    """
    f = Figlet(font='big')
    print f.renderText('HackMiner')
    print "Version 0.2.1"

def try_mine(block):
    """Updates the nonce and sees if it's valid.
    """
    block.nonce += 1
    return block.is_valid()

def mine_till_found(block):
    """Keep guessing and checking the nonce in hopes
    we mine the provided block.
    """
    print "\n\n" + ("-" * 40)
    print "Mining now with %i transactions." % len(block.transactions)
    hashes_done = 0

    start = datetime.datetime.now()
    while not try_mine(block):
        hashes_done += 1

        if hashes_done % 300000 == 0:
            end = datetime.datetime.now()
            seconds = (end - start).total_seconds()

            print "Hash Rate: %i hashes/second      \r" % (300000 / seconds),

            start = end

    print "\nMined block:", block.hash_block(), "with nonce", block.nonce

    return True

def load_wallet():
    """Load the wallet.json file and load the
    keys from there.
    """

    global public
    global private

    if os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, 'r') as f:
            wallet_json = f.read()
        wallet_obj = json.loads(wallet_json)

        public = wallet_obj['public']
        private = wallet_obj['private']
    else:
        print "First run the wallet.py file!"
        exit()

def load_transactions():
    """If there were any transactions queued by wallet.py
    we load these into a list here.
    """
    if os.path.exists(TXN_FILE):
        with open(TXN_FILE, 'r') as f:
            txn_json = f.read()
        txn_obj = jsonpickle.decode(txn_json)
        return txn_obj
    
    return []

def delete_queue(txns):
    """Remove transactions from txn_queue.json
    that we have already processed.
    """

    # These ids have already been processed.
    ids = set([t.id for t in txns])

    # Go through the transaction file.
    if os.path.exists(TXN_FILE):
        with open(TXN_FILE, 'r') as f:
            txn_json = f.read()
        
        # Read current transactions.
        txn_obj = jsonpickle.decode(txn_json)

        # Go through and delete onces we
        # haven't processed.
        new_txns = []
        for t in txn_obj:
            if t.id not in ids:
                new_txns.append(t)

        # Dump.
        with open(TXN_FILE, 'w') as f:
            f.write(jsonpickle.encode(new_txns))
        
        
def run_sample():
    """Testing code.
    """
    # Mine a sample block.
    b = Block(
        timestamp = datetime.datetime.now(),
        transactions = [],
        previous_hash = get_genisis().hash_block()
    )

    mine_till_found(b)

def run_miner():
    """Run the main miner loop.
    """

    global blockchain
    global public
    global private

    while True:
        # Load transaction queue and blockchain from server.
        txns = load_transactions()
        blockchain = load_blockchain()

        # Add reward to us yay.
        reward = Transaction(
            id = gen_uuid(),
            owner = "mined",
            receiver = public,
            coins = REWARD,
            signature = None
        )
        reward.signature = sign(reward.comp(), private)
        txns.append(reward)

        # Construct a new block.
        b = Block(
            timestamp = datetime.datetime.now(),
            transactions = txns,
            previous_hash = blockchain.head.hash_block()
        )

        # Let's mine this block.
        mine_till_found(b)

        # Is this _the_ new block?
        # or did the server swoop us :(
        new_chain = load_blockchain()

        if new_chain.head.hash_block() == blockchain.head.hash_block():
            # WE MINED THIS BLOCK YAY.
            # AND WE WIN.
            resp = get_route('add', data=str(b))
            if resp['success']:
                print "Block added!"
                delete_queue(txns)
            else:
                print "Couldn't add block:", resp['message']
        else:
            print "Someone else mined the block before us :("


if __name__ == '__main__':
    print_header()
    load_wallet()
    run_miner()