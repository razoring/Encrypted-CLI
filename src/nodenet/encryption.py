import random
import math

def isPrime(n):
    if n < 2:
        return False
    for i in range(2, n//2+1):
        if n % i == 0:
            return False
    return True

def prime(min,max):
    prime = random.randint(min,max)
    while not isPrime(prime):
        prime = random.randint(min,max)
    return prime

def modInverse(e,phi):
    for d in range(3, phi):
        if (d*e)%phi == 1:
            return d
    raise ValueError("Mod-Inverse does not exist")

p, q = prime(1000,5000), prime(1000,5000)

while p == q:
    q = prime(1000,5000)

n = p*q
phi_n = (p-1)*(q-1)

e = random.randint(3,phi_n-1)

while math.gcd(e, phi_n) != 1:
    e = random.randint(3,phi_n-1)

d = modInverse(e, phi_n)

print(e, d, n, phi_n, p, q)

msg = "Hello World"
encoded = [ord(c) for c in msg]
cipher = [pow(c, e, n) for c in encoded]

print(cipher)

encoded = [pow(c, d, n) for c in cipher]
msg = "".join(chr(c) for c in encoded)