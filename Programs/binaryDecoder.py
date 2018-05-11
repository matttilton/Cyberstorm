message = raw_input()


iteration = 0

def decode(message):
    output = ''
    i = 0
    iteration = 0
    while (i < len(message)):
        if iteration % 2 == 0:
            output += str(chr(int(message[i:i+7],2)))
            i = i + 7
            iteration += 1
        else:
            output += str(chr(int(message[i:i+8],2)))
            i = i + 8
            iteration += 1
    print output


decode(message)
