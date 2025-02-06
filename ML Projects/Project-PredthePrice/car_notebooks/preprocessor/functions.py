from deep_translator import GoogleTranslator

def translateClass(uniquevalues):
    translator = GoogleTranslator(target='en')
    rename = dict()
    for x in uniquevalues:
        rename[x] = translator.translate(x)
    print(rename)
    return rename

def getLowerCaseCharacter(text):
    return text.lower()