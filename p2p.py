import socket
import threading

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
    
    for n in peers:
        n.send(send_length)
        n.send(message)

def connect(host, port):
    addr = (host,port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(addr)
    thread = threading.Thread(target=incoming, args=addr)
    thread.start()

def incoming(conn, addr):
    print(f"Subcribed to : {addr}")

    peers.append(conn)
    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == f"Disconnected from {addr}":
                connected = False
            
            print(f"{addr}: {msg}")

    peers.remove(conn)
    conn.close()

def initiate():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen()
    print(f"Listening on {SERVER}:{PORT}")
    handleInputs()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=incoming, args=(conn, addr))
        thread.start()
        print(f"Connections: {threading.active_count()-1}")

def handleInputs():
    print("\nYour chats are encrypted.")
    while True:
        msg = input("> ")
        if msg.startswith(":help"):
            cmds = [":help - List all commands",":peers - List all connections",":connect [host]:[port] - Connect to user | Parameters:\n   ip: IPV4 Address of desired connection\n   port: Port of desired connection",":active - Expose active users on your network"]
            for cmd in cmds:
                print(cmd)
        elif msg.startswith(":connect"):
            split = msg.split(":")
            connect(split[0].strip(),split[1].strip())

if __name__ == "__main__":
    print("""Node Started. Type ":help" for a list of commands.""")
    thread = threading.Thread(target=initiate)
    thread.start()