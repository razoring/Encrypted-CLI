import random
import math
import hashlib

class RSA:
    def __init__(self, min_prime_val=1000, max_prime_val=9999):
        p = self._generate_prime(min_prime_val, max_prime_val)
        q = self._generate_prime(min_prime_val, max_prime_val)

        while p == q:
            q = self._generate_prime(min_prime_val, max_prime_val)

        self.modulus = p * q
        phi = (p - 1) * (q - 1)

        self.public_exponent = random.randint(3, phi - 1)
        while math.gcd(self.public_exponent, phi) != 1:
            self.public_exponent = random.randint(3, phi - 1)

        self.private_exponent = self._mod_inverse(self.public_exponent, phi)

    def _is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def _generate_prime(self, min_val, max_val):
        prime_candidate = random.randint(min_val, max_val)
        while not self._is_prime(prime_candidate):
            prime_candidate = random.randint(min_val, max_val)
        return prime_candidate

    def _mod_inverse(self, e, phi):
        for d in range(3, phi):
            if (d * e) % phi == 1:
                return d
        raise ValueError("Modular inverse does not exist")

    def encrypt(self, plaintext):
        encoded_chars = [ord(char) for char in plaintext]
        ciphertext = [pow(char, self.public_exponent, self.modulus) for char in encoded_chars]
        return ciphertext

    def decrypt(self, ciphertext):
        decoded_chars = [pow(char, self.private_exponent, self.modulus) for char in ciphertext]
        plaintext = "".join(chr(char) for char in decoded_chars)
        return plaintext