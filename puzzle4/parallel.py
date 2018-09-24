import datetime
import hashlib
import json
import multiprocessing
import os
import jsonpickle
import requests
from blockchain import Block, Transaction
from constants import REWARD, DIFFICULTY, TXN_FILE, WALLET_FILE, USERNAME, NODE_SERVER
from crypto import sign
from miner import load_transactions, delete_queue
from utils import gen_uuid, get_route
from wallet import load_blockchain, load_or_create

STORE_ID = "43fd78aee82fdae31c55c4cb93f8d2eb94ca8f446207be4bdca79c6ccdb54b0c"

threshold = 100


def transaction(receiver, amount, public, private):
    t = Transaction(
        id=gen_uuid(),
        owner=public,
        receiver=receiver,
        coins=amount,
        signature=None
    )

    t.signature = sign(t.comp(), private)
    txns = []
    if os.path.exists(TXN_FILE):
        with open(TXN_FILE, 'r') as f:
            txns_json = f.read()
            txns = jsonpickle.decode(txns_json)

    txns.append(t)
    with open(TXN_FILE, 'w') as f:
        f.write(jsonpickle.encode(txns))


def start_repl(public, private):
    print "Adding Transactions"
    for I in range(int(13337 / threshold) + 10):
        transaction(STORE_ID, threshold, public, private)


def processs(result, combine_block, startNonce, updateby):
    nonce = startNonce
    while result.value == -1:
        nonce += updateby
        sha = hashlib.sha256()
        sha.update(combine_block + str(nonce))
        if int(sha.hexdigest(), 16) < DIFFICULTY and result.value == -1:
            result.value = nonce


def load_wallet():
    if os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, 'r') as f:
            wallet_json = f.read()
        wallet_obj = json.loads(wallet_json)

        public = wallet_obj['public']
        private = wallet_obj['private']
        return public, private
    else:
        print "First run the wallet.py file!"
        exit()


def run_miner():
    blockchain = load_blockchain()
    public, private = load_wallet()
    uuid = gen_uuid()

    balance = blockchain.get_wallet_amount(public)

    if balance < 0:
        print "Done"
        return

    print "The balance is: " + str(balance), "hackcoins."

    txns = load_transactions()
    reward = Transaction(
        id=uuid,
        owner="mined",
        receiver=public,
        coins=REWARD,
        signature=None
    )
    reward.signature = sign(reward.comp(), private)
    txns.append(reward)

    if balance > threshold and len(txns) < 10:
        start_repl(public, private)
        txns = load_transactions()

    block = Block(
        timestamp=datetime.datetime.now(),
        transactions=txns,
        previous_hash=blockchain.head.hash_block()
    )

    print "Mining now with %i transactions." % len(block.transactions)
    print 'Time: ', datetime.datetime.now(), ' Parent Hash:  ', blockchain.head.hash_block()

    process_size = multiprocessing.cpu_count() * 2
    result = multiprocessing.Value('i', -1)
    combine_block = str(block.timestamp) + str(block.transactions) + str(block.previous_hash)
    process_array = []
    for I in range(process_size):
        process_array.append(multiprocessing.Process(target=processs, args=(result, combine_block, I, process_size)))
    for I in process_array:
        I.start()

    while result.value == -1:
        new_chain = load_blockchain()
        print 'Time: ', datetime.datetime.now(), ' Block mining: ', block.hash_block()
        if new_chain.head.hash_block() != blockchain.head.hash_block():
            result.value = -2

    block.nonce = result.value

    if result.value != -2:
        resp = get_route('add', data=str(block))
        if resp['success']:
            print "Block added!"
            delete_queue(txns)
        else:
            print "Couldn't add block:", resp['message']
    else:
        print "Someone else mined the block before us :("

    try:
        for I in process_array:
            I.terminate()
    except:
        print ""


def reset(json=True):
    endpoint = "%s/u/%s/reset" % (
        NODE_SERVER,
        USERNAME
    )

    r = requests.get(endpoint)

    if json:
        return r.json()
    else:
        # Raw
        return r.text


if __name__ == '__main__':
    print "\n"
    if os.path.exists(TXN_FILE):
        os.remove(TXN_FILE)
    if os.path.exists(WALLET_FILE):
        os.remove(WALLET_FILE)

    if reset()['success']:
        load_or_create()
        for i in range(150):
            run_miner()
