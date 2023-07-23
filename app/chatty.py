from module import gpt_utils
from module import crawl_naversearch
from app import user_settings
import re
import textwrap

text_length = 60
def print_with_line_breaks(text, line_length):

    print("\n[Agent]\n")
    sentences = re.split(r'(?<=[.])\s+', text)  # 마침표, 물음표, 느낌표를 기준으로 문장을 나눔
    wrapper = textwrap.TextWrapper(width=line_length)
    for sentence in sentences:
        lines = sentence.split('\n')  # 줄바꿈 문자를 기준으로 문장을 나눔
        for line in lines:
            wrapped_text = wrapper.wrap(line)
            for wrapped_line in wrapped_text:
                print(wrapped_line)
            print()  # 줄바꿈 추가


class Chatty():

    def __init__(self):
        print("Chatty init")
        # 네이버통검 : 블랙핑크 + 스타벅스
        contents_url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EB%B8%94%EB%9E%99%ED%95%91%ED%81%AC"
        # 뉴진스 컴백
        # contents_url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EB%89%B4%EC%A7%84%EC%8A%A4+%EC%BB%B4%EB%B0%B1"
        self.set_user()
        self.set_contents(contents_url)
        # self.req_textook()

    def set_user(self):
        self.request_setting = user_settings.make_setting()

    def set_contents(self, content_url ):
        self.content_url = content_url
        self.article_text = crawl_naversearch.get_contents( content_url )


    def req_textbook( self ):
        """
        ChatGPT 학습
        :param article_text: 기사 내용
        :param request_setting:
        :return:
        """

        print("\n### [REQ] Article summary ###\n")
        self.article_summary_text = gpt_utils.train_article_summary( self.article_text, self.request_setting)
        print_with_line_breaks(self.article_summary_text, text_length)
        return self.article_summary_text


    def req_summarized_keyword( self ):
        """
        단어 요약
        :return:
        """

        print("\n### [REQ] Article Keywords ###\n")
        question = """
        Give me 5 words in the body of the article that are difficult from an English learning perspective in "+setting_level+" without number.\n
        Don't answer with anything other than words and descriptions and Each line should be single-spaced and wrap each word in the form 'word: interpretation\n'
        """
        answer = gpt_utils.get_chatbot_response(self.article_summary_text, question, self.request_setting)
        # print(answer)
        print_with_line_breaks(answer, text_length)
        return answer

    def req_question_and_answer(self, question ):
        """
        Q&A 처리
        :param question:
        :return:
        """

        question_format = f"""
            {question}
            Please provide a short one-sentence answer to the above question and ask me a question based on the article.
        """

        print("\n### [REQ] Question and Answer ###\n")
        print( f"question : {question}" )
        answer = gpt_utils.get_chatbot_response( self.article_text, question_format, self.request_setting)
        print_with_line_breaks(answer, text_length)
        return answer

