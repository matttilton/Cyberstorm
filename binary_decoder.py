"""
Decodes a string of binary text into ascii.
Works with both 7 and 8 bit ascii.
Matthew Tilton
2017-03-25
"""
import sys

BIN_TO_DECODE = sys.stdin.readlines()[0]

def decode():
    """
        Decodes a string of binary text into ascii
    """
    is_7_bit_ascii = (len(BIN_TO_DECODE) % 7 == 0)
    is_8_bit_ascii = (len(BIN_TO_DECODE) % 8 == 0)
    output = ""
    values = []
    both_flag = False

    # Loop incase we cant tell if its 7 or 8 bit binary
    while True:
        # The actual decoding part
        if is_7_bit_ascii and is_8_bit_ascii:
            print('Cant determine bitness. Doing both')
            both_flag = True
        elif is_7_bit_ascii:
            print('Decoding as 7 bit ascii')
            values = [BIN_TO_DECODE[i:i+7] for i in range(0, len(BIN_TO_DECODE), 7)]
            for each in values:
                integer = int(each, 2)
                if integer >= 32 or integer == 8 or integer == 13 or integer == 9 or integer == 10:
                    output = output + (chr(integer))
        elif is_8_bit_ascii:
            print('Decoding as 8 bit ascii')
            values = [BIN_TO_DECODE[i:i+8] for i in range(0, len(BIN_TO_DECODE), 8)]
            for each in values:
                integer = int(each, 2)
                if integer >= 32 or integer == 8 or integer == 13 or integer == 9 or integer == 10:
                    output = output + (chr(integer))
        else:
            print('What is this shit. This isnt 7 or 8 bit ascii.')

        # Determines wheather we continue trying other ways to decode or if we are done.
        if both_flag and is_7_bit_ascii and is_8_bit_ascii:
            is_8_bit_ascii = False
        elif both_flag and is_7_bit_ascii:
            print(output)
            output = ""
            is_7_bit_ascii = False
            is_8_bit_ascii = True
        elif both_flag and is_8_bit_ascii:
            break
        else:
            break

    print(output)

decode()
