import socket
import threading

HEADER = 128
PORT = 3090
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

receipient = ""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def incoming(conn, addr):
    print(f"Connected to {addr}")
    connected = True

    while connected:
        msgLength = conn.recv(HEADER).decode(HEADER)
        if msgLength:
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(FORMAT)

            if msg == f"{addr} Disconnected":
                connected = False

            print(f"{addr}: {msg}")

    conn.close()

def start():
    server.listen()
    print(f"Listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=incoming, args=(conn,addr))
        thread.start()
        print(f"Connections: {threading.active_count()-1}")

def send(msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' '*(HEADER-len(sendLength))
    receipient.send(sendLength)
    receipient.send(message)

def input():
    print("\n Your chats are encrypted.")
    while True:
        msg:str = input("> ")
        if ":help" in msg:
            print(""":help - List all the functions\n""")


if __name__ == "__main__":
    print(f"Forwarding messages on {SERVER}")
    print("""Type ":help" to list commands.""")
    start()
    input()
    