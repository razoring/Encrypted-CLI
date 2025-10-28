import socket
import threading
import time
import argparse
import json
import os

import random
import math

class RSA:
    def __init__(self, min_prime_val=1000, max_prime_val=9999):
        p = self._prime(min_prime_val, max_prime_val)
        q = self._prime(min_prime_val, max_prime_val)

        while p == q:
            q = self._prime(min_prime_val, max_prime_val)

        self.modulus = p * q
        phi = (p - 1) * (q - 1)

        self.public_exponent = random.randint(3, phi - 1)
        while math.gcd(self.public_exponent, phi) != 1:
            self.public_exponent = random.randint(3, phi - 1)

        self.private_exponent = self._modInverse(self.public_exponent, phi)

    def _isPrime(self, n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def _prime(self, min_val, max_val):
        prime_candidate = random.randint(min_val, max_val)
        while not self._isPrime(prime_candidate):
            prime_candidate = random.randint(min_val, max_val)
        return prime_candidate

    def _modInverse(self, e, phi):
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

class Nodenet():
    def __init__(self, host, port, nickname):
        self.HEADER_LEN = 512
        self.PORT = port
        self.SERVER = host
        self.ADDR_FORMAT = (self.SERVER, self.PORT)
        self.FORMAT = "utf-8"
        self.NICKNAME = nickname

        self.peers_lock = threading.Lock()
        self.peers = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR_FORMAT)

    def _initiate(self):
        self.server.listen()
        print(f"* Listening on {self.SERVER}:{self.PORT}")

        while True:
            try:
                conn, addr = self.server.accept()
                handler = threading.Thread(target=self._connections, args=(conn, addr))
                handler.daemon = True
                handler.start()
            except OSError:
                break

    def _connections(self, conn, addr):
        print(f"* Subscribed to {addr}")

        with self.peers_lock:
            self.peers.append(conn)
        
        connected = True
        while connected:
            try:
                header = conn.recv(self.HEADER_LEN)
                if not header:
                    connected = False
                    continue

                header_data = json.loads(header.decode(self.FORMAT).strip())
                length = int(header_data["length"])
                nickname = header_data["nickname"]
                msg = conn.recv(length).decode(self.FORMAT)

                print(f"\n[{nickname}]: {msg}\n> ", end="")

            except (ConnectionResetError, json.JSONDecodeError, ValueError, OSError):
                connected = False

        with self.peers_lock:
            if conn in self.peers:
                self.peers.remove(conn)
        conn.close()

    def connect(self, host, port: int):
        try:
            addr = (host, port)
            peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer.connect(addr)

            connection = threading.Thread(target=self._connections, args=(peer, addr))
            connection.daemon = True
            connection.start()
        except (ConnectionRefusedError, socket.gaierror, TimeoutError):
            print(f"* Failed to connect to {host}:{port}")

    def _send(self, msg):
        message = msg.encode(self.FORMAT)
        sendLen = json.dumps({
            "nickname": self.NICKNAME,
            "length": len(message)
        }).encode(self.FORMAT)
        
        header = sendLen + b' ' * (self.HEADER_LEN - len(sendLen))

        with self.peers_lock:
            for peer in list(self.peers):
                try:
                    peer.send(header)
                    peer.send(message)
                except socket.error:
                    self.peers.remove(peer)

    def _inputs(self):
        print("\n* Your chats are encrypted.")

        while True:
            time.sleep(1/100)
            msg = input("> ")
            if not msg:
                continue

            if msg == ":help":
                cmds = [":help - List all commands",":peers - List all connections",":connect <host>:<port> - Connect to user",":close - Disconnect from network"]
                for cmd in cmds:
                    print(cmd)
            elif msg.startswith(":connect"):
                try:
                    split = msg.replace(":connect ", "").split(":")
                    self.connect(split[0].strip(), int(split[1].strip()))
                except (ValueError, IndexError):
                    print("* Invalid command format.")
            elif msg == ":peers":
                with self.peers_lock:
                    print(f"* {len(self.peers)} Active Connections:")
                    for peer in self.peers:
                        try:
                            print("    " + str(peer.getpeername()))
                        except OSError:
                            continue
            elif msg == ":close":
                self.close()
                break
            else:
                self._send(msg)

    def boot(self):
        print(f"* Node started as {self.NICKNAME}")
        print("""* Type ":help" for a list of commands.""")

        thread = threading.Thread(target=self._initiate)
        thread.daemon = True
        thread.start()
        self._inputs()

    def close(self):
        print("* Network disconnected")
        self.server.close()
        os._exit(0)

def main():
    parser = argparse.ArgumentParser(description="Start a Nodenet Chat")
    parser.add_argument("--port", type=int, default=5050, help="Port to listen on. (default: 5050)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="IPV4 Address to bind to. (default: 0.0.0.0)")
    parser.add_argument("--nickname", type=str, required=True, help="Nickname to display (required)")
    args = parser.parse_args()
    node = Nodenet(host=args.host, port=args.port, nickname=args.nickname)
    node.boot()