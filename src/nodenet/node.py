import socket
import threading
import time
import argparse
import json
import os

import random
import math

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
    
    def encrypt(self, msg, publicKey):
        ascii = [ord(char) for char in msg]
        cipher = [pow(char, publicKey, self.n) for char in ascii]
        return cipher

    def decrypt(self, cipher, privateKey):
        ascii = [pow(char, privateKey, self.n) for char in cipher]
        msg = "".join(chr(char) for char in ascii)
        return msg

class Nodenet():
    def __init__(self, host, port, nickname):
        self.HEADER_LEN = 512
        self.PORT = port
        self.SERVER = host
        self.ADDR_FORMAT = (self.SERVER, self.PORT)
        self.FORMAT = "utf-8"
        self.NICKNAME = nickname

        self.publicKey = 0
        self.privateKey = 0
        self.encrypt = encryption()

        self.peers = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR_FORMAT)

    def _initiate(self):
        self.publicKey, self.privateKey = self.encrypt.generateKeyPair()

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

        connected = True

        #recieving
        while connected:
            try:
                header = conn.recv(self.HEADER_LEN)
                if not header:
                    connected = False
                    continue

                header_data = json.loads(header.decode(self.FORMAT).strip())
                length = int(header_data["length"])
                nickname = header_data["nickname"]
                key = header_data["key"]

                if not conn in self.peers:
                    self.peers = self.peers.update({conn:key})

                msg = self.encrypt.decrypt(conn.recv(length).decode(self.FORMAT), self.privateKey)

                print(f"\n[{nickname}]: {msg}\n> ", end="")

            except (ConnectionResetError, json.JSONDecodeError, ValueError, OSError):
                connected = False

        if conn in self.peers:
            del self.peers[conn]
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

    def _send(self, msg, key):
        message = self.encrypt.encrypt(msg.encode(self.FORMAT))
        sendLen = json.dumps({
            "nickname": self.NICKNAME,
            "length": len(message),
            "key": self.publicKey
        }).encode(self.FORMAT)
        
        header = sendLen + b' ' * (self.HEADER_LEN - len(sendLen))

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