import boto3
import os
from module import date_utils
from config import WEB_HOME_PATH

class AWSUtils():

    def __init__(self):
        self.polly_client = boto3.Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_ID"),
            region_name='ap-northeast-2').client('polly')
        # self.request_tts_download( text='hello my name is yuna.')

    # 참고 : https://docs.aws.amazon.com/ko_kr/polly/latest/dg/SynthesizeSpeechSamplePython.html
    def request_tts_download( self, text, voice_id = 'Joanna', engine = 'neural' ):

        try:
            now_time = date_utils.now_date_str('%Y%m%d_%H%M%S')
            filepath = f"/mp3/{now_time}.mp3"
            file_full_path = f'{WEB_HOME_PATH}/{filepath}'

            print(f"[REQ] TTS, filepath = {file_full_path}, text = {text}")
            response = self.polly_client.synthesize_speech(VoiceId=voice_id, OutputFormat='mp3', Text = text, Engine = engine )

            file = open( file_full_path, 'wb')
            file.write(response['AudioStream'].read())
            file.close()
            print(f"[REQ] TTS download completed.")
            return filepath
        except Exception as e :
            print(f"Exception : TTS message = {e}")
            return None

        # voice
        # [Lotte, Maxim, Ayanda, Salli, Ola, Arthur, Ida, Tomoko, Remi, Geraint, Miguel, Elin, Lisa, Giorgio, Marlene, Ines,
        #  Kajal, Zhiyu, Zeina, Suvi, Karl, Gwyneth, Joanna, Lucia, Cristiano, Astrid, Andres, Vicki, Mia, Vitoria, Bianca,
        #  Chantal, Raveena, Daniel, Amy, Liam, Ruth, Kevin, Brian, Russell, Aria, Matthew, Aditi, Zayd, Dora, Enrique, Hans,
        #  Hiujin, Carmen, Sofie, Ivy, Ewa, Maja, Gabrielle, Nicole, Filiz, Camila, Jacek, Thiago, Justin, Celine, Kazuha,
        #  Kendra, Arlet, Ricardo, Mads, Hannah, Mathieu, Lea, Sergio, Hala, Tatyana, Penelope, Naja, Olivia, Ruben, Laura,
        #  Takumi, Mizuki, Carla, Conchita, Jan, Kimberly, Liv, Adriano, Lupe, Joey, Pedro, Seoyeon, Emma, Niamh, Stephen]


    # 참고 : https://github.com/awslabs/amazon-transcribe-streaming-sdk
    def request_transcribe(self):
        print("ASR")