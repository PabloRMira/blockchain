"Blockchain dummy example"

from dataclasses import dataclass
from datetime import datetime
import hashlib
import random
from typing import List

from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA


@dataclass
class Transaction:
    amount: float
    payer: str
    payee: str

    def to_string(self) -> str:
        return str(self)


@dataclass
class Block:
    previous_hash: str
    transaction: Transaction
    ts: str = str(datetime.now())
    nonce: int = random.randint(0, 100000) * 99999999999999

    @property
    def hash(self) -> str:
        block_str = str(self).encode("utf-8")
        hasher = hashlib.sha256()
        hasher.update(block_str)
        return hasher.hexdigest()


class Chain:
    chain: List[Block] = [Block("", Transaction(100, "genesis", "satoshi"))]

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    @staticmethod
    def mine(nonce: int) -> int:
        solution = 1
        print("🔨  mining...")

        while True:
            hasher = hashlib.md5()
            hasher.update(str(nonce + solution).encode("utf-8"))
            attempt = hasher.hexdigest()
            if attempt[0:4] == "0000":
                print(f"Solved: {solution}")
                break
            solution += 1

        return solution

    def add_block(
        self, transaction: Transaction, sender_public_key: str, signature: bytes
    ) -> None:
        sender_public_key_ = RSA.import_key(sender_public_key)
        verifier = pkcs1_15.new(sender_public_key_)
        hasher = SHA256.new()
        hasher.update(transaction.to_string().encode("utf-8"))
        try:
            verifier.verify(hasher, signature)
            is_valid = True
        except ValueError:
            is_valid = False

        if is_valid:
            new_block = Block(self.last_block.hash, transaction)
            self.mine(new_block.nonce)
            self.chain.append(new_block)


class Wallet:
    def __init__(self):
        keypair = RSA.generate(2048)
        self.public_key = keypair.public_key().export_key()
        self.private_key = keypair.export_key()

    def send_money(self, amount: float, payee_public_key: str, chain: Chain) -> None:
        transaction = Transaction(amount, self.public_key, payee_public_key)

        hasher = SHA256.new()
        hasher.update(transaction.to_string().encode("utf-8"))
        private_key = RSA.import_key(self.private_key)
        signer = pkcs1_15.new(private_key)
        signature = signer.sign(hasher)

        chain.add_block(transaction, self.public_key, signature)


def main() -> None:
    chain = Chain()
    satoshi = Wallet()
    bob = Wallet()
    alice = Wallet()

    satoshi.send_money(50, bob.public_key, chain)
    satoshi.send_money(23, alice.public_key, chain)
    satoshi.send_money(5, bob.public_key, chain)

    print(chain.chain)


if __name__ == "__main__":
    main()
 