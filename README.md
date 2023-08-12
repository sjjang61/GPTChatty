# Intro
- Chatty with GPT(openai) based on web-socket 
- https://marvelous-bramble-54c.notion.site/1ec59b9d720b4d26b9a0b8d19b85e7b8
- client-sample : http://54.180.109.21/, https://www.chatties.shop/
- .env : setting local environment  

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

