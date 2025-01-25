from hashlib import sha256
from binascii import hexlify

hashes = []

def merkel(num):
    global hashes
    if num==1:
        return hashes[0]
    if num%2==1:
        hashes[num] = hashes[num-1]
        num += 1
    for i in range(0, num, 2):
        concat = hashes[i] + hashes[i+1]
        concat = hexlify(concat.encode())
        hash = sha256(concat).hexdigest()
        hashes[i//2] = hash
    return merkel(num//2)

if __name__ == "__main__":
    for _ in range(0, int(input())):
        strings = int(input())
        for _ in range(0, strings):
            hash = sha256(input().encode()).hexdigest()
            hashes.append(hash)
        hashes.append("")
        print(merkel(strings))
