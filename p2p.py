import socket
import threading
import time

HEADER = 128
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

peers = []

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))
    
    for peer in peers:
        peer.send(send_length)
        peer.send(message)
        #print(f"Sent to {peer}")

def connect(host, port:int):
    addr = (host,port)
    peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer.connect(addr)
    thread = threading.Thread(target=connection, args=(peer, addr))
    thread.start()

def connection(conn, addr):
    print(f"* Subcribed to {addr}")

    peers.append(conn)
    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            #print(f"Recieved from {addr}")
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == f"* Disconnected from {addr}":
                connected = False
            
            print(f"{addr}: {msg}")

    peers.remove(conn)
    conn.close()

def initiate():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen()
    print(f"* Listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=connection, args=(conn, addr))
        thread.start()
        print(f"Connections: {len(peers)}")

def inputs():
    print("\n* Your chats are encrypted.")
    while True:
        time.sleep(0.01)
        msg = input("> ")
        if msg == (":help"):
            cmds = [":help - List all commands",":peers - List all connections",":connect <host>:<port> - Connect to user | Parameters:\n   ip: IPV4 Address of desired connection\n   port: Port of desired connection",":active - Expose active users on your network"]
            for cmd in cmds:
                print(cmd)
        elif msg.startswith(":connect"):
            split = msg.replace(":connect ","").split(":")
            connect(split[0].replace(" ","").strip(),int(split[1].replace(" ","").strip()))
        elif msg == (":peers"):
            print(f"* {len(peers)} Active Connections:")
            for peer in peers:
                print("    "+str(peer.getpeername()))
        else:
            send(msg)

if __name__ == "__main__":
    print("""* Node Started. Type ":help" for a list of commands.""")
    thread = threading.Thread(target=initiate)
    thread.start()

    inputs()