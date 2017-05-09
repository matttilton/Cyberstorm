"""
Vigenere cypher encode and decoder
"""
import sys
import argparse
from random import SystemRandom

def main():
    """
    Program starting point
    """
    parser = argparse.ArgumentParser(prog='Vigenere', description='Encrypts and decrypts '
                                     + 'input using a vigenere cypher')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--decrypt', help='Decrypts a string using the provided key.')
    group.add_argument('-e', '--encrypt', help='Encrypts a string using the provided key.')
    group.add_argument('-g','--generate-one-time-pad', help='Generates a one time pad with a length of N characters. Use -f to specify an output file. Otherwise, will output to OTP.txt')
    parser.add_argument('-f', '--file', help='Specify input or output file. This will override the key parameter for both -d and -e.')
    args = parser.parse_args()
    # print(args)
    if(args.decrypt != None):
        while True:
            #Gracefully handle KeyboardInterrupt and EOFError
            try:
                text = input(':')
                print(decrypt(args.decrypt, text, args.file))
            except KeyboardInterrupt:
                print('\r')
                sys.exit()
            except EOFError:
                print('\r')
                sys.exit()
    elif(args.encrypt != None):
        while True:
            #Gracefully handle KeyboardInterrupt and EOFError
            try:
                text = input(':')
                print(encrypt(args.encrypt, text, args.file))
            except KeyboardInterrupt:
                print('\r')
                sys.exit()
            except EOFError:
                print('\r')
                sys.exit()
    elif (args.generate_one_time_pad != None):
        #Gracefully handle KeyboardInterrupt and EOFError
        try:
            one_time_pad_generator(args.generate_one_time_pad, args.file)
        except KeyboardInterrupt:
            print('\r')
            sys.exit()
        except EOFError:
            print('\r')
            sys.exit()

def encrypt(key, plaintext, filename):
    """
    Encrypts plaintext using a key. Returns cyphertext.
    """
    #sanitizing key
    key = key.lower() #Comment this out after submitting
    key = key.replace(" ", "")

    #use one time pad if specified
    #overrides provided key
    if filename != None:
        f = open(filename, "r+")
        try:
            key = f.readlines()[0]
        except IndexError:
            print('Key file is empty')
            sys.exit()
        f.close()

    outputstring = ''

    #apply offset to every character based on the key provided
    for i in range(0, len(plaintext)):
        plaintextLetter = ord(plaintext[i])
        if plaintextLetter != 32:
            keyLetter = ord(key[i%len(key)]) #convert from ascii to int
            keyLetter = ((keyLetter % 26) - 19)
            
            #sanitize plaintext to get letters below 26
            if plaintext[i].islower():
                plaintextLetter = ((plaintextLetter % 26) - 19)
            else:
                plaintextLetter = ((plaintextLetter % 26) - 13)
            
            #apply key offset
            newLetter = (plaintextLetter + keyLetter) % 26

            if plaintext[i].islower(): #add offset for capital or lowercase letters
                newLetter = newLetter + 97
            else:
                newLetter = newLetter + 65
        else:
            newLetter = 32
            
        outputstring = outputstring + chr(newLetter) #convert from int to ascii and add to output

    #remove used bits of the key from one time pad if it is used
    if filename != None:
        f = open(filename, "w")
        key = key[len(outputstring):]
        f.write(key)    
        f.close()
    
    return(outputstring)

def decrypt(key, cyphertext, filename):
    """
    Decrypts cyphertext using a key. Returns plaintext.
    """
    #decrypt is nearly identical to encrypt. see encrypt for comments
    key = key.lower()
    key = key.replace(" ", "")
    outputstring = ''

    if filename != None:
        f = open(filename, "r+")
        try:
            key = f.readlines()[0]
        except IndexError:
            print('Key file is empty')
            sys.exit()
        f.close()

    for i in range(0, len(cyphertext)):
        cyphertextLetter = ord(cyphertext[i])
        if cyphertextLetter != 32:
            keyLetter = ord(key[i%len(key)])
            keyLetter = ((keyLetter % 26) - 19)
            if cyphertext[i].islower():
                cyphertextLetter = ((cyphertextLetter % 26) - 19)
            else:
                cyphertextLetter = ((cyphertextLetter % 26) - 13)

            newLetter = (cyphertextLetter - keyLetter) % 26 #this is the only different line between encrypt and decrypt. here we subtract the offset instead of add.

            if cyphertext[i].islower():
                newLetter = newLetter + 97
            else:
                newLetter = newLetter + 65
        else:
            newLetter = 32
            
        outputstring = outputstring + chr(newLetter)
    
    if filename != None:
        f = open(filename, "w")
        key = key[len(outputstring):]
        f.write(key)    
        f.close()
    
    return(outputstring)

def one_time_pad_generator(length, file):
    """
    Generates large one time pads of random characters.
    """
    #work in progress
    randomCharList = []
    outputString = ''
    for i in range(int(length)):
        randomCharList.append(SystemRandom().randrange(26))
    for i in range(0, len(randomCharList)):
            outputString = outputString + chr(randomCharList[i] % 26 + 97)

    if (file != None):
        f = open(file, "w+")
    else:
        f = open("OTP.txt", "w+")
    
    f.write(outputString)

main()
