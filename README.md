# Nodenet: Privacy made simple
A **peer-to-peer** chat service secured with **end-to-end RSA encryption** that runs in your CLI. Chat individually or in groups with unlimited connections.

## Chat Securely
When a connection is established, a public and private key are generated and the public keys are exchanged by each connection. a Encryption is secured by the client using a unique public key and decryption is handled by the receipient using their unique private key. Keys are randomly generated integers between **1000 to 99 999** — which is **98 000** unique possible keys.

#### Chats do not save.
# Getting Started
## Installation
```
pip install nodenetwork
```
## Initialization
```
nodenet --host <address> --port <port> --nickname <nickname>
```

#### Example:
```
nodenet --host 127.0.0.1 --port 1234 --nickname razoring
```

#### List of CLI Commands
- **host -** Accessible IPV4 address to host **your** node (default: localhost)
- **port -** Accessible port address to host **your** node  (default: 5050)
- **nickname -** Any string of characters **(REQUIRED)**
- **help -** List all available CLI commands

# Usage
```
* Node started as razoring
* Type ":help" for a list of commands.

> <input>
```
#### List of Commands
- **:connect <host\>:<port\> -** Connect to a user via their IP and port separated by a colon
- **:peers -** List all active connections
- **:close -** Disconnect from network

#### Usage Example:
```
* Node started as razoring
* Type ":help" for a list of commands.

> :connect 127.0.0.1:5050
* Secure handshake with ('127.0.0.1', 5050) successful

* Your chats are encrypted.
* Subscribed to ('127.0.0.1', 5050)

> Hello World
[Other]: Hello razoring!
> :help
    :help - List all commands
    :peers - List all connections
    :connect <host>:<port> - Connect to user
    :close - Disconnect from network
> :close
* Network disconnected
```