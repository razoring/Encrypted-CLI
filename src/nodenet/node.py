import socket
import threading
import time
import argparse
import json
import random

class Nodenet():
    def __init__(self, host, port, nickname):
        self.HEADER_LEN = 512
        self.PORT = port
        self.SERVER = host
        self.ADDR_FORMAT = (self.SERVER, self.PORT)
        self.FORMAT = "utf-8"
        self.NICKNAME = nickname

        self.peers = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR_FORMAT)

    def _initiate(self):
        self.server.listen()
        print(f"* Listening on {self.SERVER}:{self.PORT}")

        while True:
            conn, addr = self.server.accept()
            handler = threading.Thread(target=self._connections, args=(conn,addr,self.NICKNAME))
            handler.start()

    def _connections(self, conn, addr, nickname):
        print(f"* Subscribed to {addr}")

        self.peers.append(conn)
        connected = True

        while connected:
            header = conn.recv(self.HEADER_LEN).decode(self.ADDR_FORMAT)
            if header:
                length = int(json.loads(header)["length"])
                msg = conn.recv(length).decode(self.ADDR_FORMAT)

                if msg == f"* Disconnected from {nickname}":
                    connected = False

                print(f"{nickname}: {msg}")
        
        self.peers.remove(conn)
        conn.close()

    def connect(self, host, port:int):
        addr = (host,port)
        peer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        peer.connect(addr)

        connection = threading.Thread(target=self._connections, args=(peer,addr))
        connection.start()

    def _send(self, msg):
        message = msg.encode(self.FORMAT)
        sendLen = json.dumps({
            "nickname":self.NICKNAME,
            "length":str(len(msg))
        }).encode(self.FORMAT)
        header = b' '*(self.HEADER_LEN-len(sendLen))

        for peer in self.peers:
            peer.send(header)
            peer.send(message)

    def _inputs(self):
        print("\n* Your chats are encrypted.")

        while True:
            time.sleep(1/100)
            msg = input("\n> ")

            if msg == ":help":
                cmds = [":help - List all commands",":peers - List all connections",":connect <host>:<port> - Connect to user | Parameters:\n   ip: IPV4 Address of desired connection\n   port: Port of desired connection",":close - Disconnect from network"]
                for cmd in cmds:
                    print(cmd)
            elif msg.startswith(":connect"):
                split = msg.replace(":connect ","").split(":")
                self.connect(split[0].replace(" ","").strip(),int(split[1].replace(" ","").strip()))
            elif msg == (":peers"):
                print(f"* {len(self.peers)} Active Connections:")
                for peer in self.peers:
                    print("    "+str(peer.getpeername()))
            elif msg == (":close"):
                self._send(f"* Disconnected from {self.NICKNAME}")
                self.close()
            else:
                self._send(msg)

    def boot(self):
        print(f"* Node started as {self.NICKNAME}")
        print("""* Type ":help" for a list of commands.""")

        thread = threading.Thread(target=self._initiate)
        thread.start()
        self._inputs()
    
    def close(self):
        print("* Network disconnected")
        self.server.close()

def main():
    parser = argparse.ArgumentParser(description="Start a Nodenet Chat")
    parser.add_argument("--port", type=int, default=5050, help="Port to listen on. (default: 5050)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="IPV4 Address to bind to. (default: 127.0.0.1)")
    parser.add_argument("--nickname", type=str, required=True, help="Nickname of length <=10. (default:random)")
    args = parser.parse_args()
    node = Nodenet(host=args.host,port=args.port,nickname=args.nickname)
    node.boot()
