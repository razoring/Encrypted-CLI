import math
import random

class encryption():
    def __init__(self, min=1000, max=9999):
        self.MIN = min
        self.MAX = max
        self.privateKey = 0
        self.publicKey = 0

        self.n = 0

    def _generatePrime(self):
        prime = random.randint(self.MIN,self.MAX)
        while not self._isPrime(prime):
            prime = random.randint(self.MIN,self.MAX)
        return prime

    def _isPrime(self, n):
        if n < 2:
            return False
        for i in range(2, n//2+1):
            if n%i == 0:
                return False
        return True
    
    def _inverseMod(self, e, phi):
        for d in range(3, phi):
            if (d*e)%phi == 1:
                return d
        raise ValueError("Mod-inverse does not exist")
    
    def generateKeyPair(self):
        p = q = self._generatePrime()
        while p == q:
            q = self._generatePrime()
        phi_N = (p-1)*(q-1)

        self.n = p*q

        self.publicKey = random.randint(3, phi_N-1)
        while math.gcd(self.publicKey, phi_N) != 1:
            self.publicKey = random.randint(3, phi_N-1)
        
        self.privateKey = self._inverseMod(self.publicKey, phi_N)

        return self.publicKey, self.privateKey
    
    def encode(self, msg, publicKey):
        ascii = [ord(char) for char in msg]
        cipher = [pow(char, publicKey, self.n) for char in ascii]
        return cipher

    def decode(self, cipher, privateKey):
        ascii = [pow(char, privateKey, self.n) for char in cipher]
        msg = "".join(chr(char) for char in ascii)
        return msg
    
e = encryption()
pub, priv = e.generateKeyPair()

msg = e.encode("hello world", pub)
print(msg)
new = e.decode(msg, priv)
print(new)