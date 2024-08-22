import requests
from bs4 import BeautifulSoup
from googletrans import Translator


def get_english_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)
#        print(response.text)

        soup = BeautifulSoup(response.content, "html.parser")
        english_words = soup.find("div", id="random_word").text.strip()
        word_definition = soup.find("div", id="random_word_definition").text.strip()

        return {
            "english_words": english_words,
            "word_definition": word_definition
        }
    except Exception as e :
        print("Произошла ошибка:(e)")
        return None


def translate_to_russian(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='ru')
    return translation.text


def word_game():
    print("Добро пожаловать в игру")
    while True:
        word_dict = get_english_words()

        if word_dict is None:
            print("Не удалось получить слово. Попробуйте ещё раз.")
            continue
        word = word_dict.get("english_words")
        word_definition = word_dict.get("word_definition")

        translated_word = translate_to_russian(word)
        translated_definition = translate_to_russian(word_definition)

        print(f"Значение слова - {translated_definition}")
        user = input("Что это за слово? (Введите слово на русском) ")
        if user.lower() == translated_word.lower():
            print("Все верно")
        else:
            print(f"Ответ неверный, было загадано это слово - {translated_word}")

        play_again = input("Хотите сыграть ещё раз? д/н ")
        if play_again != "д":
            print("Спасибо за игру!")
            break


word_game()
