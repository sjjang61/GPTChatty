import openai

# OpenAI API 인증
openai.api_key = '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'  # 여기에 API 키를 입력하세요.
text_length = 60
OPENAI_MODEL = "gpt-3.5-turbo"

def train_article_model(article_text,request):
    """
    기사 텍스트를 학습
    :param article_text:
    :param request:
    :return:
    """

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
        model = OPENAI_MODEL,
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
        model= OPENAI_MODEL,
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
        model = OPENAI_MODEL,
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt}
        ]
    )

    # ChatGPT의 답변 반환
    return response['choices'][0]['message']['content']
