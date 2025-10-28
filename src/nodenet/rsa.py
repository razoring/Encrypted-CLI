import math
import random

def isPrime(n):
        if n < 2:
            return False
        for i in range(2, n//2+1):
            if n%i == 0:
                return False
        return True
    
def genPrime(min, max):
    prime = random.randint(min,max)
    while not isPrime(prime):
        prime = random.randint(min,max)
    return prime

def modInverse(e, phi):
    for d in range(3, phi):
        if (d*e)%phi == 1:
            return d
    raise ValueError("Mod Inverse does not exist")

p, q = genPrime(1000,5000), genPrime(1000,5000)
while p == q:
    q = genPrime(1000,5000)

n = p*q
phi_n = (p-1)*(q-1)

pubKey = random.randint(3, phi_n-1)
while math.gcd(pubKey, phi_n) != 1:
    pubKey = random.randint(3, phi_n-1)

privKey = modInverse(pubKey, phi_n)

msg = "Hello World"
msgEncoded = [ord(char) for char in msg]
cipher = [pow(char, pubKey, n) for char in msgEncoded]
print(cipher)
msgEncoded = [pow(char, privKey, n) for char in cipher]
msg = "".join(chr(char) for char in msgEncoded)
print(msg)