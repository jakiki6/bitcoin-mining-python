import os, hashlib, binascii
def get_sha_256_hash(input_value):
    return hashlib.sha256(input_value).hexdigest()
def fwz(i, l): #Fill with zero
    if len(i) > l:
        return i[:l]
    while len(i) != l:
        i = "0" + i
    return i

while True:
    block = os.path.join("blocks", "block_" + fwz(input("Which Block ID?: "), 20)) + ".blk"
    try:
        open(block, "r")
    except Exception as e:
        print("This block ID doesn\'nt exist!")
        continue
    blockFile = open(block, "r")
    blockRaw = blockFile.read() [2:]
    blockData = blockRaw [128:len(blockRaw) - 64]
    blockNonce = blockRaw [len(blockRaw) - 64:]
    blockTargetHash = blockRaw [64:128]
    blockBeforeHash = blockRaw [:64]
    blockHash = get_sha_256_hash(get_sha_256_hash(hex(int(blockRaw.replace("0x", ""), 16)).encode()).encode())
    blockData = binascii.unhexlify((blockData).encode()).decode().replace(binascii.unhexlify("00".encode()).decode(), "")
    print("Block data:")
    print(blockData)
    print("Block hash:")
    print(blockHash)
    print("Target hash:")
    print(blockTargetHash)
    print("Hash of block before:")
    print(blockBeforeHash)
    print("Nonce:")
    print(blockNonce)