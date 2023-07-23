
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
def make_setting():
    setting_language = make_choice('Language',1, ["English", "Japanese", "Chinese"])
    setting_level = make_choice('Level', 2, ["Advanced", "Intermediate", "Beginner"])
    setting_tone = make_choice('Tone', 3, ["Friend", "professor", "co-worker"])
    setting_article = make_choice('Article', 4, ["Economy", "Culture", "Entertainment"])

    request_setting = f"""
        You are an {setting_language} assistant with an English level of {setting_level}. 
        Speak like a {setting_tone}. 
        Make all your answers conversational.
    """
    return request_setting