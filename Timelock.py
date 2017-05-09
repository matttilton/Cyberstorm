"""
Matthew Tilton
5-3-2017
Simple timelock algorithm for csc442.
test script can be found on github at
https://github.com/matttilton/coursework/blob/master/csc442/Timelock/timelocktest.sh
"""
import fileinput
from datetime import datetime, date
import hashlib
import time
import sys

# consant declaration
# setting debug to True will get current times from the second line of
# the input
USE_SYSTEM_TIME = False
DEBUG = False


def isletter(char):
    """
    checks a character and determines if it is a letter
    """
    char = ord(char)
    if char >= 65 and char <= 122 and not 91 <= char <= 96:
        return True


def isnumber(char):
    """
    checks a character and determines if it is a number
    """
    char = ord(char)
    if 48 <= char <= 57:
        return True


def rudimentary_dst_check(datestr):
    """
    Very simple check for DST does not account for early morning on dst day
    also does not account for dst being on the first sunday of the month before 2007.
    Doesnt account for the inconsistent application that was going on before 1967,
    but I dont think those last two issues will be a problem since the entire
    program is based off of epoch time and will output unintended results if given
    a time before that. Probably. Basically dont put anything before 1970ish and
    you will probably be fine. Unless... Daylight Savings Time is complicated.
    """
    date_time_date = date(int(datestr[0]), int(datestr[1]), int(datestr[2]))
    prev_sun = int(datestr[2]) - date_time_date.weekday()
    # check for jan feb dec
    if int(datestr[1]) < 3 or int(datestr[1]) > 11:
        return False
    # check for apr to oct
    if int(datestr[1]) > 3 and int(datestr[1]) < 11:
        return True
    # check if after second sunday
    if int(datestr[1]) == 3:
        return prev_sun >= 7
    # otherwise its november check if before first sunday
    return prev_sun <= 0


def main():
    """
    main function. pylint is happy now.
    """

    # set default current time value
    current_time = "2017 05 04 12 57 34"

    # read input from stdin
    input_file = fileinput.input()

    # read and parse epoch from stdin
    epoch_array = input_file[0].rstrip().split(' ')
    epoch_dst = rudimentary_dst_check(epoch_array)
    epoch_date = datetime(int(epoch_array[0]), int(epoch_array[1]), int(
        epoch_array[2]), int(epoch_array[3]), int(epoch_array[4]), int(epoch_array[5]))

    # sets current time as second line of input if debug is enabled
    if DEBUG:
        current_time = input_file[1].rstrip()

    # determines wheather or not to use system time of time from file
    # if time comes from file it is parsed
    if USE_SYSTEM_TIME:
        current_time_date = datetime.now()
        current_time_dst = time.daylight
    else:
        current_time_array = current_time.split(' ')
        current_time_dst = rudimentary_dst_check(current_time_array)
        current_time_date = datetime(int(current_time_array[0]), int(current_time_array[1]), int(
            current_time_array[2]), int(current_time_array[3]), int(current_time_array[4]),
            int(current_time_array[5]))

    # calculates the current number of seconds that have elapsed since the
    # epoch
    epoch_seconds_from_real_epoch = (
        epoch_date - epoch_date.utcfromtimestamp(0)).total_seconds()
    current_seconds_from_real_epoch = (
        current_time_date - current_time_date.utcfromtimestamp(0)).total_seconds()

    # apply dst offsets if neccesary
    if current_time_dst:
        current_seconds_from_real_epoch = current_seconds_from_real_epoch - 3600
    if epoch_dst:
        epoch_seconds_from_real_epoch = epoch_seconds_from_real_epoch - 3600

    # epoch_seconds_from_real_epoch = time.mktime(epoch_date.timetuple())
    # current_seconds_from_real_epoch = time.mktime(current_time_date.timetuple())
    timediff = int(round(current_seconds_from_real_epoch -
                         epoch_seconds_from_real_epoch))
    timediff = timediff - (timediff % 60)

    # hashes the timedifference between the current time and the fake epoch
    # twice
    md5 = hashlib.md5(hashlib.md5(str(timediff)).hexdigest()).hexdigest()

    result_code = ''

    # loops through the hash and finds the first two letters
    # then appends them to result_code in the order that they are found
    letter_counter = 0
    for each in md5:
        if letter_counter >= 2:
            break

        if isletter(each):
            result_code = result_code + each
            letter_counter = letter_counter + 1

    # in the unlikely event that there are not enough letters, increase the
    # amount of numbers to find
    numbers_needed = 2 + (2 - letter_counter)

    # loop though the reverse of the md5 hash and append the first two numbers
    # to result_code
    number_counter = 0
    for each in md5[::-1]:
        if number_counter >= numbers_needed:
            break

        if isnumber(each):
            result_code = result_code + each
            number_counter = number_counter + 1

    # if we do not find enough numbers then go back through the hash and find the next letters
    # until result_code has 4 characters
    if number_counter < 2:
        secondletter_counter = 0
        for each in md5:
            if secondletter_counter > letter_counter:
                result_code = result_code + each
            else:
                secondletter_counter = secondletter_counter + 1
            if len(result_code) >= 4:
                break

    # print to stdout dont include newline if debuging
    if DEBUG:
        sys.stdout.write(result_code)
        sys.stdout.flush()
    else:
        sys.stdout.write(result_code + "\n")
        sys.stdout.flush()


main()
