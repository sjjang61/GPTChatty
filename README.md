# Intro
- Chatty with GPT(openai) based on web-socket 
- https://marvelous-bramble-54c.notion.site/1ec59b9d720b4d26b9a0b8d19b85e7b8
- client-sample : http://54.180.109.21/, https://www.chatties.shop/
- .env : setting local environment
- websocket : https://github.com/dpallot/simple-websocket-server/blob/master/README.md

```python
TLS/SSL Example
1. Generate a certificate with key (for localhost)
penssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem

2. Run the secure TLS/SSL server (in this case the cert.pem file is in the same directory)
python SimpleExampleServer.py --example chat --ssl 1 --cert ./cert.pem

3. Offer the certificate to the browser by serving websocket.html through https. The HTTPS server will look for cert.pem in the local directory. Ensure the websocket.html is also in the same directory to where the server is run.
sudo python SimpleHTTPSServer.py

4. Open a web browser to: https://localhost:443/websocket.html

5. Change ws://localhost:8000/ to wss://localhost:8000 and click connect.
```

```python
OPENAI_API_KEY="..."
AWS_ACCESS_KEY_ID="..."
AWS_SECRET_ACCESS_ID="..."
AWS_SESSION_TOKEN=""
```

## Protocol
- defined in protocol.py
```python

    # CLI -> SVR
    # SVR -> CLI (xxx_ACK)    

    START_CLASS = auto()       # 수업시작
    START_CLASS_ACK = auto()

    TEXTBOOK = auto()           # 텍스트북(교재)
    TEXTBOOK_ACK = auto()

    CHAT_MSG = auto()
    CHAT_MSG_ACK = auto()

    END_CLASS = auto()         # 수업종료

```

