# https://github.com/dpallot/simple-websocket-server
# pip install SimpleWebSocketServer
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from app.chatty import Chatty
from app.protocol import Command
from dotenv import load_dotenv
from module import gpt_utils
from module import aws_utils

import json
import os

clients = []
class SimpleChat(WebSocket):

    def handleMessage(self):

        print('[Message] From : %s, Payload : %s' % (self.address[0], self.data))
        msg = json.loads(self.data)
        self.recvMsgHandler(msg['cmd'], msg['params'])

        # for client in clients:
        #     if client != self:
        #         client.sendMessage(self.address[0] + u' - ' + self.data)

    def recvMsgHandler(self, cmd, params):
        """
        메시지 처리 및 응답
        cmd (str) : command
        params (object) : json 데이터
        """

        print("[RecvMessage] cmd = %r, params = %r" % (cmd, params))
        send_data = {'cmd': cmd + "_ACK" }

        if cmd == Command.TEXTBOOK.name:

            print(f"[REQ] textbook, contents = {params['url']}")
            chatty.set_contents( params['url'] )
            answer = chatty.req_textbook()
            tts_path = aws_utils.request_tts_download( text=answer )

            send_data['data' ] = { 'contents' : answer, 'tts_path' : tts_path  }
            self.sendMessage( json.dumps( send_data ) )

        elif cmd == Command.CHAT_MSG.name:

            print(f"[REQ] chatting, msg = {params['msg']}")
            answer = chatty.req_question_and_answer( params['msg'] )

            send_data['data' ] = {'msg': answer }
            self.sendMessage( json.dumps( send_data ) )

        else:
            print('[ERROR] Unknown Command : %s' % (cmd))
            send_data['data'] = {'msg': 'Unknown Command'}
            self.sendMessage(json.dumps(send_data))

    def handleConnected(self):
       print(self.address, 'connected')

       for client in clients:
          client.sendMessage(self.address[0] + u' - connected')

       clients.append(self)

    def handleClose(self):
       clients.remove(self)
       print(self.address, 'closed')
       for client in clients:
          client.sendMessage(self.address[0] + u' - disconnected')

# .env 환경변수 로드
load_dotenv()
gpt_utils.set_api_key( os.getenv("OPENAI_API_KEY") )

server = SimpleWebSocketServer('', 8888, SimpleChat)
print("start server")

chatty = Chatty()
server.serveforever()