from random import randrange


# Password generator function
def PassProcess(passwordLength, unicodeToggle):
    charList = []
    password = ""
    if unicodeToggle == "1":
        for x in range(passwordLength - 10):
            character = randrange(31, 55296)
            charList.append(character)
        for x in range(10):
            character = randrange(31, 126)
            charList.append(character)
    else:
        for x in range(passwordLength):
            character = randrange(31, 126)
            charList.append(character)

    for x in range(len(charList)):
        passwordCharacter = chr(charList[x])
        password = password + passwordCharacter
    return password
