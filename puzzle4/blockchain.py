import hashlib
import json
import crypto
import datetime
import constants
import jsonpickle

class Transaction:
    def __init__(self, id, owner, receiver, coins, signature):
        self.owner = owner
        self.receiver = receiver
        self.coins = coins
        self.id = id
        self.signature = signature

    def valid_signature(self):
        if self.owner == "mined":
            return True
        return crypto.verify(self.comp(), self.owner, self.signature)

    def __str__(self):
        return json.dumps({
            'owner': self.owner,
            'receiver': self.receiver,
            'coins': self.coins,
            'id': self.id,
            'signature': self.signature
        })

    def comp(self):
        return json.dumps({
            'owner': self.owner,
            'receiver': self.receiver,
            'coins': self.coins,
            'id': self.id
        })

    def __repr__(self):
        return str(self)

    @staticmethod
    def from_json(jobj):
        return Transaction(
            id = str(jobj['id']),
            owner = str(jobj['owner']),
            receiver = str(jobj['receiver']),
            coins = int(jobj['coins']),
            signature = str(jobj['signature'])
        )

class Block:
    def __init__(self, timestamp, transactions, previous_hash, nonce=0, height=-1):
        self.height = height
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce

        self.parent = None

        # Transaction lookup
        self.txn_lookup = {}
        for transaction in self.transactions:
            self.txn_lookup[transaction.comp()] = True

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.txn_lookup[transaction.comp()] = True

    def set_parent(self, parent):
        self.parent = parent
        self.height = parent.height + 1
    
    def hash_block(self):
        sha = hashlib.sha256()

        sha.update(str(self.timestamp) + 
                   str(self.transactions) + 
                   str(self.previous_hash) + 
                   str(self.nonce))

        return sha.hexdigest()

    def __str__(self):
        return json.dumps({
            'timestamp': str(self.timestamp),
            'transactions': str(self.transactions),
            'previous_hash': str(self.previous_hash),
            'nonce': self.nonce
        })

    def is_valid(self):
        return int(self.hash_block(), 16) < constants.DIFFICULTY

    def traverse(self, include_head=True):
        """Goes recursively through parents.
        """
        if include_head:
            yield self
        current = self.parent
        genisis_hash = get_genisis().hash_block()
        while current != None and current.hash_block() != genisis_hash:
            yield current
            current = current.parent

    @staticmethod
    def from_json(jobj):
        return Block(
            timestamp = datetime.datetime.strptime(jobj['timestamp'], "%Y-%m-%d %H:%M:%S.%f"),
            transactions = [
                Transaction.from_json(tj)
                for tj in json.loads(jobj['transactions'])
            ],
            previous_hash = str(jobj['previous_hash']),
            nonce = int(jobj['nonce'])
        )

def get_genisis():
    return Block(
        height = 0,
        timestamp = datetime.datetime.min,
        transactions = [],
        previous_hash = None
    )

class Blockchain:
    def __init__(self, json_str=None):
        if json_str:
            pass
        else:
            blocks = [get_genisis()]

        # Lookup
        self.head = blocks[0]
        self.block_lookup = {}
        for b in blocks:
            self.block_lookup[b.hash_block()] = b
            if b.height > self.head.height:
                self.head = b

        # Parents
        for b in blocks:
            if not b.previous_hash == None:
                assert b.previous_hash in self.block_lookup
                b.set_parent(self.block_lookup[b.previous_hash])

    def get_wallet_amount(self, address):
        total = 0

        # Go back through the current longest chain
        # and tally the total.
        for b in self.head.traverse(include_head=True):
            if not b:
                break

            for txn in b.transactions:
                if txn.owner == address and txn.receiver != address:
                    total -= txn.coins
                elif txn.owner != address and txn.receiver == address:
                    total += txn.coins

        return total

    def add_block(self, block, cheat=False):
        """Checks the entire chain for valid transactions
        and checks proof of work. Then adds block."""

        block_hash = block.hash_block()

        # We already know this block.
        if block_hash in self.block_lookup:
            return False, "Known block."
        
        # Parent doesn't exist :(
        if block.previous_hash not in self.block_lookup:
            return False, "No valid parent."
        parent = self.block_lookup[block.previous_hash]
        
        block.set_parent(parent)

        # Check proof of work ;o
        if not cheat and not block.is_valid():
            return False, "Invalid proof of work."

        # Verify transaction signatures.
        for transaction in block.transactions:
            if transaction.owner != "mined" and not transaction.valid_signature():
                return False, "Transaction has invalid signature."

        # Have any of these transactions been replays?
        for b in block.traverse(include_head=True):
            for c_txn in block.transactions:
                if c_txn in b.txn_lookup:
                    # We found the same transaction in a previous block.
                    return False, "Transaction replay detected."
        
        # For every transaction, does the owner own this money?
        reward_counted = False
        for txn in block.transactions:
            if txn.coins < 0:
                return False, "Amount can't be negative."
                
            if txn.owner == "mined":
                # This is the miner reward, let's make sure
                # it's correct. Technically, the miner can make
                # this payment to anyone she likes.
                if txn.coins > constants.REWARD:
                    return False, "Incorrect miner reward."
                
                # Let's also make sure the reward is only given
                # once and once only.
                if reward_counted:
                    return False, "Miner reward found twice in block."

                reward_counted = True
            else:
                owner_coins = self.get_wallet_amount(txn.owner)
                if owner_coins < txn.coins:
                    # Owner doesn't have enough coins,
                    # block is invalid.
                    return False, "Owner doesn't have enough coins."
        
        # Looks like everything is set with this block.
        # Let's add this block and compute the longest
        # chain.

        self.block_lookup[block_hash] = block
        if block.height > self.head.height:
            self.head = block
        
        return True, "Block added."

    def to_json(self):
        return jsonpickle.encode(self)

if __name__ == '__main__':
    # Just a sanity test.
    bc = Blockchain()
    bc.add_block(
        Block(
            timestamp=datetime.datetime.now(),
            transactions=[],
            previous_hash=get_genisis().hash_block(),
            nonce=12834
        ),
        cheat=True
    )
    print(bc.to_json())
