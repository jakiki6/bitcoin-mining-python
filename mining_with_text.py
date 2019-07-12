import hashlib, random, os, binascii

def get_start_rand():
    t = ""
    for _ in range(16 * 30):
        t += random.choice("0 1 2 3 4 5 6 7 8 9 a b c d e f".split(" "))
    return t
    
def get_sha_256_hash(input_value):
    return hashlib.sha256(input_value).hexdigest()


def block_hash_less_than_target(block_hash, given_target):
    return int(block_hash, 16) < int(given_target, 16)
def fwz(i, l): #Fill with zero
    if len(i) > l:
        return i[:l]
    while len(i) != l:
        i = "0" + i
    return i

# Initial block data
blockData = (\
    '0000000000000000000000000000000000000000000000000000000000000000' \
    '0000000000000000000000000000000000000000000000000000000000000000' + get_start_rand()).encode()

highest_number = "-1"
for _, _, f in os.walk("blocks"):
    for file in f:
        if "block_" in file:
            highest_number = file.replace("block_", "").replace(".blk", "")
if not highest_number == "-1":
    file = open(os.path.join("blocks", "block_") + highest_number + ".blk", "r")
    blockData = file.read().encode()
    file.close()
    print("Start with block " + highest_number)

# Initial target - this is the easiest it will ever be to mine a Bitcoin block
target = '0x0008FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'

#Init hash
if highest_number == "-1":
    last_hash = get_sha_256_hash("".encode())
else:
    tmpfile = open(os.path.join("blocks", "block_") + highest_number + ".blk", "r")
    last_hash = tmpfile.read() [:64]
    tmpfile.close()
    del(tmpfile)


def reset():
    global solution_found, block_data_hexadecimal_value, nonce
    solution_found = False
    block_data_hexadecimal_value = str(hex(int(blockData, 16)))
    nonce = 0
reset()
if highest_number == "-1":
    counter = 0
else:
    counter = int(highest_number)
while True:
    block_data_with_nonce = block_data_hexadecimal_value + fwz(str(nonce), 64)

    # Find double hash
    first_hash = get_sha_256_hash(hex(int(block_data_with_nonce, 16)).encode())
    second_hash = get_sha_256_hash(first_hash.encode())
    solution_found = block_hash_less_than_target(second_hash, target)
    if not solution_found:
        nonce += 1
    else:
        #print(nonce)
        print(block_data_with_nonce)
        file = open(os.path.join("blocks", "block_") + fwz(str(counter), 20) + ".blk", "w")
        file.write(block_data_with_nonce)
        file.close()
        blockData = last_hash + fwz(str(hex(int(target, 16))).replace("x", ""), 64) + fwz(binascii.hexlify(input("Data?: ").encode()).decode(), 29 * 64)
        reset()
        counter += 1
        last_hash = second_hash
