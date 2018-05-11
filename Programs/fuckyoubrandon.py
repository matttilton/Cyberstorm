import sys

bintodecode = input()
result = ''
i = 0
def checksevenbit():
    global bintodecode
    global result
    global i
    firstseven = bintodecode[i:i+7]
    try:
        integer = int(firstseven, 2)
    except:
        integer = 32
    character = chr(integer)
    if character.isdigit() or character == ' ':
        result = result + character
        i=i+7
    else:
        checkeightbit()

def checkeightbit():
    global bintodecode
    global result
    global i
    firstseven = bintodecode[i:i+8]
    try:
        integer = int(firstseven, 2)
    except:
        integer = 32
    character = chr(integer)
    if character.isdigit() or character == ' ':
        result = result + character
        i = i+8
    else:
        print('fuck')


while len(bintodecode) > 7:
    checksevenbit()

print(result)