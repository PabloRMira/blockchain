import crypto from "crypto";

class Transaction {
  constructor(
    public amount: number,
    public payer: string,
    public payee: string
  ) {}

  toString(): string {
    return JSON.stringify(this);
  }
}

class Block {
  public nonce = Math.round(Math.random() * 99999999);

  constructor(
    public prevHash: string,
    public transaction: Transaction,
    public ts = new Date().toISOString()
  ) {}

  get hash(): string {
    const str = JSON.stringify(this);
    const hash = crypto.createHash("SHA256");
    hash.update(str).end();
    return hash.digest("hex");
  }
}

class Chain {
  public chain: Block[];

  constructor() {
    this.chain = [new Block("", new Transaction(100, "genesis", "satoshi"))];
  }

  get lastBlock(): Block {
    return this.chain[this.chain.length - 1];
  }

  mine(nonce: number): number {
    let solution = 1;
    console.log("⛏  mining...");

    while (true) {
      const hash = crypto.createHash("MD5");
      hash.update((nonce + solution).toString()).end();
      const attempt = hash.digest("hex");
      if (attempt.substring(0, 4) === "0000") {
        console.log(`Solved: ${solution}`);
        return solution;
      }
      solution += 1;
    }
  }

  addBlock(
    transaction: Transaction,
    senderPublicKey: string,
    signature: Buffer
  ): void {
    const verify = crypto.createVerify("SHA256");
    verify.update(transaction.toString());

    const isValid = verify.verify(senderPublicKey, signature);

    if (isValid) {
      const newBlock = new Block(this.lastBlock.hash, transaction);
      this.mine(newBlock.nonce);
      this.chain.push(newBlock);
    }
  }
}

class Wallet {
  public publicKey: string;
  public privateKey: string;

  constructor() {
    const keypair = crypto.generateKeyPairSync("rsa", {
      modulusLength: 2048,
      publicKeyEncoding: { type: "spki", format: "pem" },
      privateKeyEncoding: { type: "pkcs8", format: "pem" },
    });

    this.publicKey = keypair.publicKey;
    this.privateKey = keypair.privateKey;
  }

  sendMoney(amount: number, payeePublicKey: string, chain: Chain): void {
    const transaction = new Transaction(amount, this.publicKey, payeePublicKey);

    const sign = crypto.createSign("SHA256");
    sign.update(transaction.toString()).end();

    const signature = sign.sign(this.privateKey);
    chain.addBlock(transaction, this.publicKey, signature);
  }
}

const main = (): void => {
  const chain = new Chain();
  const satoshi = new Wallet();
  const bob = new Wallet();
  const alice = new Wallet();

  satoshi.sendMoney(50, bob.publicKey, chain);
  bob.sendMoney(23, alice.publicKey, chain);
  alice.sendMoney(5, bob.publicKey, chain);

  console.log(chain);
};

main();
