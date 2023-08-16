# https://github.com/dpallot/simple-websocket-server
# pip install SimpleWebSocketServer
import argparse
import ssl
import signal
import sys
import logging
from SimpleWebSocketServer import SimpleWebSocketServer, SimpleSSLWebSocketServer, WebSocket
from app.chatty import Chatty
from app.protocol import Command
from dotenv import load_dotenv
from module import gpt_utils
from module.aws_utils import AWSUtils
# from app.file_transfer import TransferFile

import json
import os

logger = logging.getLogger(__name__)
clients = []
class SimpleChat(WebSocket):

    def handleMessage(self):

        print('[Message] From : %s, Payload : %s' % (self.address[0], self.data))
        try:
            # decoded_data = self.data.decode('utf-8')
            msg = json.loads( self.data )
            self.recvMsgHandler(msg['cmd'], msg['params'])
        except Exception as e:
            print("[Exception] json load, error = ", e )

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

            send_data['data' ] = { 'contents' : answer  }
            self.sendMessage( json.dumps( send_data ) )

        elif cmd == Command.CHAT_MSG.name:

            print(f"[REQ] chatting, msg = {params['msg']}")
            answer = chatty.req_question_and_answer( params['msg'] )
            tts_path = aws_utils.request_tts_download(text=answer)

            send_data['data' ] = {'msg': answer, 'tts_path' : tts_path }
            self.sendMessage( json.dumps( send_data ) )

        elif cmd == Command.FILE_TRANSFER_HEADER.name:

            print(f"[REQ] FILE_TRANSFER_HEADER, filename = {params['filename']}, filesize = {params['filesize']}")
            # file.filename = params['filename']
            # file.filesize = params['filesize']
            print("header complete")

        elif cmd == Command.FILE_TRANSFER_BODY.name:

            data = params['data']
            print(f"[REQ] FILE_TRANSFER_BODY, filedata = ")
            # file.add_data( data )
            print("body complete")


        elif cmd == Command.FILE_TRANSFER_END.name:
            print(f"[REQ] FILE_TRANSFER_END")
            # file.save()
            # file.reset()
            print(f"end complete")

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

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ht", "--host", required=False, default='')
    parser.add_argument("-pt", "--port", required=False, default= 8888)
    parser.add_argument("-ssl", "--ssl", required=False, default= False, type=bool)
    parser.add_argument("-cert", "--cert", required=False, default= "cert.pem")
    parser.add_argument("-key", "--key", required=False, default= "key.pem")
    parser.add_argument("-ver", "--ver", required=False, default= ssl.PROTOCOL_TLSv1_2, type=int, help="ssl version")

    args = parser.parse_args()
    # logger.info("[Configure]")

    print("[Configure]")
    logger.info("")
    print("============================================")
    print("\t- Host : %s" % (args.host))
    print("\t- Port : %s" % (args.port))
    print("\t- SSL : %s" % (args.ssl ))
    print("\t- Cert : %s" % (args.cert))
    print("\t- Key : %s" % (args.key))
    print("\t- Version : %d" % (args.ver))
    print("============================================")
    return args

if __name__ == "__main__":
    args = arg_parse()

    # .env 환경변수 로드
    load_dotenv()
    gpt_utils.set_api_key( os.getenv("OPENAI_API_KEY") )
    aws_utils = AWSUtils()

    if args.ssl == False:
        server = SimpleWebSocketServer( args.host, args.port, SimpleChat)
        print("start websocket server")
    else:
        server = SimpleSSLWebSocketServer( args.host, args.port, SimpleChat, args.cert, args.key )
        print("start websocket server(SSL)")

    chatty = Chatty()
    # file = TransferFile()

    def close_sig_handler(signal, frame):
        server.close()
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)
    server.serveforever()