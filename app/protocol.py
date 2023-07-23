import json
from enum import Enum, auto


def get_msg_format(self, cmd, data):
    msg = {
        "command": cmd,
        "data": data
    }
    return json.dumps(msg)

'''
Message Format(json)

1) CLT --> SVR 

{
   "command" : "...",
   "params" : { ... },
}

2) SVR --> CLT  

{
   "command" : "...",
   "params" : { ... },
}
'''

class Command(Enum):
    # CLT -> SVR
    # CONNECT
    START_CLASS = auto()       # 수업시작
    START_CLASS_ACK = auto()

    TEXTBOOK = auto()           # 텍스트북(교재)
    TEXTBOOK_ACK = auto()

    CHAT_MSG = auto()
    CHAT_MSG_ACK = auto()

    END_CLASS = auto()         # 수업종료

    # SVR -> CLT
    TEXTBOOK_SEND = auto()
