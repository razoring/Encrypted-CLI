# Nodenet
A **peer-to-peer** chat service secured with **end-to-end RSA encryption** that runs in your CLI.

# Getting Started
## Installation
```
pip install nodenet
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