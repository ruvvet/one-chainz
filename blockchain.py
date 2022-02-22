import time
import block 

class Blockchain:

    # ?????????????????
    difficulty = 1

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        # self.difficulty = 1

    # the first block
    def create_genesis_block(self):
        # make a new block
        genesis_block = block.Block(0, [], time.time(), "0")
        # hash the block
        genesis_block.hash = genesis_block.compute_hash()
        # append block
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        block.nonce = 0
        # compute hash
        computed_hash = block.compute_hash()
        # if its not genesis block, add + 1 difficulty
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce +=1
            computed_hash = block.compute_hash()
        return computed_hash


    def add_block(self,block, proof ):
        # get prev hash
        prev_hash = self.last_block.hash
        # validation?
        if prev_hash != block.prev_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        # otherwise its good
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        ## valid if the difficulty matches? (multily string x #????)
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
                self.unconfirmed_transactions.append(transaction)
    
    def mine(self):
            if not self.unconfirmed_transactions:
                return False
    
            last_block = self.last_block
    
            new_block = block.Block(index=last_block.index + 1,
                            transactions=self.unconfirmed_transactions,
                            timestamp=time.time(),
                            previous_hash=last_block.hash)
    
            proof = self.proof_of_work(new_block)
            self.add_block(new_block, proof)
            self.unconfirmed_transactions = []
            return new_block.index