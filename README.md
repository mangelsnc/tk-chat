# tk-chat

🗨️ Chat with TKinter

# Bootstraping

## Generate certificate for SSL cipher

### 1. Generate key

```shell
openssl genpkey -algorithm RSA -out server-key.key -aes256
```

### 2. Generete Certificate Signature Request

```shell
openssl req -new -key server-key.key -out server.csr
```

**Important!** Set `localhost` as `Common Name`

### 3. Generate Certificate

```shell
openssl x509 -req -days 365 -in server.csr -signkey server-key.key -out server-cert.pem
```

### 4. Remove password from key

```shell
openssl rsa -in server-key.key -out server-key.key
```

## Start server

You can start the server simply by executing it:

```shell
./server.py
```

or 

```shell
python3 ./server.py
```

## Start client

You can start the client simply by executing it:

```shell
./client.py
```

or 

```shell
python3 ./client.py
```

