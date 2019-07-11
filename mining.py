import hashlib, random

def get_start_rand():
    t = ""
    for _ in range(16 * 30):
        t += random.choice("0 1 2 3 4 5 6 7 8 9 a b c d e f".split(" "))
    return t
    
def get_sha_256_hash(input_value):
    return hashlib.sha256(input_value).hexdigest()


def block_hash_less_than_target(block_hash, given_target):
    return int(block_hash, 16) < int(given_target, 16)
def fwz(i, l):
    if len(i) > l:
        return i[:l]
    while len(i) != l:
        i = "0" + i
    return i

# Initial block data (the transactions' merkle tree root, timestamp, client version, hash of the previous block)
blockData = (\
    '01000000000000000000000000000000000000000000000000000000000000000000000' \
    '03ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f' + get_start_rand()).encode()

# Initial target - this is the easiest it will ever be to mine a Bitcoin block
target = '0x00008FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'

def reset():
    global solution_found, block_data_hexadecimal_value, nonce
    solution_found = False
    block_data_hexadecimal_value = int(blockData, 16)
    nonce = 0
reset()
counter = 0
while True:
    block_data_with_nonce = block_data_hexadecimal_value + nonce

    # Find double hash
    first_hash = get_sha_256_hash(hex(block_data_with_nonce).encode())
    second_hash = get_sha_256_hash(first_hash.encode())
    solution_found = block_hash_less_than_target(second_hash, target)
    if not solution_found:
        nonce += 1
    else:
        #print(nonce)
        blockData = second_hash + fwz(str(nonce), 32) + fwz("0", 16 * 30)
        print(blockData)
        file = open("./blocks/block_" + fwz(str(counter), 20) + ".blk", "w")
        file.write(blockData)
        file.close()
        reset()
        counter += 1
