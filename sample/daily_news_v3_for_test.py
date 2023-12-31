# -*- coding: utf-8 -*-
"""(이승민)Daily News v3 for test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AjbygdJ01wxe-A6Q814RE2AgC1XamOJb

# **사전 설정**

**OpenAI 설치**
"""

# !pip install openai

"""**BeautifulSoup 로딩**"""
#
import requests
from bs4 import BeautifulSoup
import time
#
# ## https://velog.io/@sh97818/Crawling-%EB%84%A4%EC%9D%B4%EB%B2%84-%EB%89%B4%EC%8A%A4-%EB%B3%B8%EB%AC%B8-%ED%81%AC%EB%A1%A4%EB%A7%81

response = requests.get("https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EB%B8%94%EB%9E%99%ED%95%91%ED%81%AC&oquery=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&tqi=hyYPFlprvmsss4UxVAhssssssg4-385087")
html = response.text
soup = BeautifulSoup(html, "html.parser")
articles = soup.select("div.info_group")

for article in articles:
    links = article.select("a.info")
    if len(links) >= 2:
        url = links[1].attrs["href"]
        response = requests.get(url, headers={'User-agent': 'Mozila/5.0'})      # to avoid error use headers
        html = response.text                                                    # for each url get html
        soup = BeautifulSoup(html, "html.parser")                               # for each html make soup

        # separation
        if "entertain" in response.url:                                         # to avoid redirection error
            title = soup.select_one(".end_tit")                                 # get the title
            content = soup.select_one("#articeBody")                            # get the body
        else:
            title = soup.select_one(".media_end_head_headline")                 # get the title
            content = soup.select_one("#dic_area")                              # get the body

        print("========LINK========\n", url)
        print("========TITLE========\n", title.text.strip())
        print("========BODY========\n", content.text.strip())
        time.sleep(0.3)

        break;
article_text = content.text.strip()

"""**사용자 셋팅 항목 선택**"""

def make_choice(category,number,options):
    print("{}.[{}] Please select one of the following options:".format(number,category))
    print()
    for i, option in enumerate(options):
        print(f"  {chr(65+i)}. {option}")
    print()
    #choice = input("  Enter the letter of your choice: ").upper()
    choice = "A"
    if choice in [chr(65+i) for i in range(len(options))]:
        index = ord(choice) - 65
        selected_option = options[index]
        print(f"  You selected <{selected_option}>")

    else:
        print("  Invalid choice. Please try again.")
    print()
    return selected_option


# 사용 예시

setting_language = make_choice('Language',1,["English", "Japanese", "Chinese"])
setting_level = make_choice('Level'   ,2,["Advanced", "Intermediate", "Beginner"])
setting_tone = make_choice('Tone'    ,3,["Friend", "professor", "co-worker"])
setting_article = make_choice('Article' ,4,["Economy", "Culture", "Entertainment"])

print("setting parameter : ",setting_language,"/",setting_level,"/",setting_tone,"/",setting_article)
print()

"""**함수 정의**"""

#good - 제목 요약에 대해서만 일본어 처리 가능하도록

import openai
import re
import textwrap

#request_setting = "Your answers must be in "+ setting_language +" and the level to be " + setting_level +". Speak like a " + setting_tone +". write all your answers in sentences."
request_setting = "You are an "+ setting_language +" assistant with an English level of " + setting_level +". Speak like a " + setting_tone +". Make all your answers conversational."

# OpenAI API 인증
openai.api_key = 'OPEN_API_KEY'  # 여기에 API 키를 입력하세요.
text_length = 60
#article_text = "article : Donghae Water and Baekdu Mountain to dry up and wear out"

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


def train_chat_model(article_text,request):
    # 기사 텍스트를 학습시키는 prompt
    pre_sentence = """
    Summarize the following article in three simple sentences in "+setting_language +".
    After printing your summary, print '### example conversation ###'.
    Provide an additional example of a conversation between two 20-somethings based on the article.
    Organize them into 10 consecutive questions and answers.
    """
    #keyword = "and Let us know which "+setting_level+" words in the article caught your eye. Please wrap each word in the form 'word: interpretation' and Wrap every other word "
    prompt = pre_sentence + "\n\n" + article_text
    # ChatGPT에 대화 학습 요청
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": request},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # 학습된 모델 반환
    return response['choices'][0]['message']['content']

def get_chatbot_response(article_text, question, request):
    # 질문을 ChatGPT에 전달하는 prompt
    prompt = question + "\n\n"

    # ChatGPT에 질문 전달
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": request},
            {"role": "system", "content": article_text},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=235,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0

    )

    # ChatGPT의 답변 반환
    return response['choices'][0]['message']['content']

def get_chatbot_response_comple(article_text, question, request):
    # 질문을 ChatGPT에 전달하는 prompt
    prompt = question + "\n\n" + request
    # ChatGPT에 질문 전달
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt}
        ]
    )

    # ChatGPT의 답변 반환
    return response['choices'][0]['message']['content']

"""# **기사 Q&A**"""



#@title
###
debug_mode = 0


# Setting 출력
print("Setting info : ",request_setting)

# ChatGPT 학습
print("\n\n\n### Article summary ###")
trained_model = train_chat_model(article_text,request_setting)
print_with_line_breaks(trained_model, text_length)

# 단어 요약
print("\n\n\n### Key words ###")
question = """
Give me 5 words in the body of the article that are difficult from an English learning perspective in "+setting_level+" without number.\n
Don't answer with anything other than words and descriptions and Each line should be single-spaced and wrap each word in the form 'word: interpretation\n'
"""

answer = get_chatbot_response(trained_model, question, request_setting)
#print(answer)
print_with_line_breaks(answer, text_length)

# 문답 3회
debug_mode = 1 # 0 : debug(pre-question), 1 : user

question_list = []
print("\n\n\n### Conversation ###")
print("\n[You]\n")
if debug_mode==1 :
  question = "What is the title?"
else :
  question = input()
question_list.append(question)
print("\n")

print( question )
answer = get_chatbot_response(article_text, question +"/n Please provide a short one-sentence answer to the above question and ask me a question based on the article.",request_setting)
print_with_line_breaks(answer, text_length)


print("\n[You]\n")
if debug_mode==1 :
  question = "What is the topic of article?"
else :
  question = input()
question_list.append(question)
print("\n")

print( question )
answer = get_chatbot_response(article_text, question +"/n Please provide a short one-sentence answer to the above question and ask me a question based on the article.",request_setting)
print_with_line_breaks(answer, text_length)


print("\n[You]\n")
if debug_mode==1 :
  question = "what is your opinion about this article"
else :
  question = input()
question_list.append(question)
print("\n")

print( question )
answer = get_chatbot_response(article_text, question +"/n Please provide a short one-sentence answer to the above question and ask me a question based on the article.",request_setting)
print_with_line_breaks(answer, text_length)

# 보정된 질문 보여주기

question_list_comple = []
question_comple = "Please revise the following sentence between the <> to be more elegant."

print("\n\n\n### Question calibration ###")
for i in range(len(question_list)):

    print("\n[You]\n")
    print(question_list[i])
    question = question_comple + "\n<" + question_list[i] +">"
    answer = get_chatbot_response_comple(article_text, question, "")

    print_with_line_breaks(answer, text_length)
    question_list_comple.append(answer)

