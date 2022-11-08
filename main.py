import requests
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("native_language",
                    help="You need to choose the language to translate from.")

parser.add_argument("translate_language",
                    help="You need to choose the language to translate to.")

parser.add_argument("text",
                    help="The word that needs to be translated.")

languages = {
    '1': 'arabic',
    '2': 'german',
    '3': 'english',
    '4': 'spanish',
    '5': 'french',
    '6': 'hebrew',
    '7': 'japanese',
    '8': 'dutch',
    '9': 'polish',
    '10': 'portuguese',
    '11': 'romanian',
    '12': 'russian',
    '13': 'turkish'
}
args = parser.parse_args()

native_language = args.native_language
translate_language = args.translate_language
text = args.text
f = open(text + '.txt', 'w+', encoding="utf-8")


def console_part():
    print('Hello, welcome to the translator. Translator supports: ')
    print("1. Arabic")
    print("2. German")
    print("3. English")
    print("4. Spanish")
    print("5. French")
    print("6. Hebrew")
    print("7. Japanese")
    print("8. Dutch")
    print("9. Polish")
    print("10. Portuguese")
    print("11. Romanian")
    print("12. Russian")
    print("13. Turkish")
    print("Type the number of your language: ")
    global native_language
    native_language = input()

    print("Type the number of a language you want to translate to or '0' to translate to all languages: ")
    global translate_language
    translate_language = input()
    print("Type the word you want to translate: ")
    global text
    text = input()
    global f
    f = open(text + '.txt', 'w+', encoding="utf-8")


headers = {'User-Agent': 'Mozilla/5.0'}


def get_url(word):
    return f"https://context.reverso.net/translation/" + native_language + '-' + translate_language + '/' + word


def extract_translated_words(bs_obj):
    translations = [a.text.strip() for a in bs_obj.find_all('a', class_="translation")][1:]
    return translations


def extract_examples(bs_obj):
    examples = []
    for elem in bs_obj.find_all('div', class_='example'):
        examples.append(":\n".join(x.text.strip() for x in elem.find_all('span', class_='text')))
    return examples


def print_translations(soup, count):
    global f
    words = extract_translated_words(soup)
    for i in range(count):
        find = str(words[i]).find(' ')
        if find != -1:
            print(str(words[i])[0:find])
            f.writelines(str(words[i])[0:find] + '\n')
        else:
            print(str(words[i]))
            f.writelines(str(words[i]) + '\n')


def print_examples(soup, count):
    global f
    sentences = extract_examples(soup)
    for i in range(count):
        print(sentences[i])
        print()
        f.write(sentences[i] + '\n')
        f.write('\n')


def translate():
    global native_language, translate_language, text
    try:
        assert native_language in languages.values(), "Sorry, the program doesn't support " + native_language

        if translate_language == 'all':
            for i in range(1, 14):

                translate_language = languages.get(str(i))
                page = requests.get(get_url(text), headers=headers)
                if page.status_code == 404:
                    raise ConnectionError('Sorry, unable to find' + text)
                assert page.status_code == 200, 'Something wrong with your internet connection'

                soup = BeautifulSoup(page.content, 'html.parser')
                if native_language != translate_language:
                    f.write(translate_language.title() + ' Translations:\n')
                    print(translate_language.title() + ' Translations:')

                    print_translations(soup, 1)
                    f.write('\n' + translate_language.title() + ' Examples:\n')
                    print('\n' + translate_language.title() + ' Examples:')
                    print_examples(soup, 1)
                    print()
                    f.write('\n')

        else:
            assert translate_language in languages.values(), "Sorry, the program doesn't support " + translate_language

            page = requests.get(get_url(text), headers=headers)
            if page.status_code == 404:
                raise ConnectionError('Sorry, unable to find' + text)

            assert page.status_code == 200, 'Something wrong with your internet connection'

            soup = BeautifulSoup(page.content, 'html.parser')

            f.write(translate_language.title() + ' Translations:\n')
            print(translate_language.title() + ' Translations:')
            print_translations(soup, 5)
            f.write('\n' + translate_language.title() + ' Examples:\n')
            print('\n' + translate_language.title() + ' Examples:')
            print_examples(soup, 5)

    except AssertionError as err:
        print(err)
    except ConnectionError as err:
        print(err)

    f.close()


def main():
    translate()


if __name__ == "__main__":
    main()
