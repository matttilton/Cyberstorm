"""
Matthew Tilton
2017-04-10

Gets the file permissions from the files on a ftp server and converts them into readable binary.
"""
import time
from ftplib import FTP

filePermissions = []
binaryPermissions = ''

#converts binary to ascii
def convertBinaryToAscii():
    output = ''

    #decodes as 7 bit ascii
    tmp = binaryPermissions[:(len(binaryPermissions) - (len(binaryPermissions) % 7))] #strips of trailing bits that dont fit into a multiple of 8
    values = [tmp[i:i+7] for i in range(0, len(tmp), 7)] #splits string into multiples of 7bits
    for each in values:
        integer = int(each, 2)#converts from binary into decimal
        if integer >= 32 or integer == 8 or integer == 13 or integer == 9 or integer == 10: #checks for printable characters
            output = output + (chr(integer))

    # error checking
    flag = False
    for each in output:
        if ord(each) > 128 or ord(each) < 8 or 14 <= ord(each) <= 31: # Checking for invalid characters
            flag = True
        if (len(output) * 7) != len(tmp): # Checking for invalid lengths
            flag = True

    if (not flag):
        print output

    #decodes as 8 bit ascii
    output = '' #reset output
    tmp = binaryPermissions[:len(binaryPermissions) - (len(binaryPermissions) % 8)] #strips of trailing bits that dont fit into a multiple of 8
    values = [tmp[i:i+8] for i in range(0, len(tmp), 8)] #splits string into multiples of 8 bits
    for each in values:
        integer = int(each, 2) #converts from binary into decimal
        if integer >= 32 or integer == 8 or integer == 13 or integer == 9 or integer == 10: #checks for printable characters
            output = output + (chr(integer))

    # error checking
    flag = False
    for each in output:
        if ord(each) > 128 or ord(each) < 8 or 14 <= ord(each) <= 31: #checking for invalid characters
            flag = True
        if (len(output) * 8) != len(tmp): #checking for invalid lengths
            flag = True

    if (not flag):
        print output

#converts the permissions to binary
def convertPermissionsToBinary():
    global binaryPermissions
    #converts the file permissions to binary assuming that all permissions are important
    for x in filePermissions:
        for i in x: #for each letter in each permision string
            if (i != '-'):
                binaryPermissions = binaryPermissions + '1'
            else:
                binaryPermissions = binaryPermissions + '0'
    convertBinaryToAscii() #converts the binary to ascii
    binaryPermissions = ''
    for x in filePermissions:
        if (x[0] != '-' or x[1] != '-' or x[2] != '-'): #ignore files that have the first 3 bits set
            pass
        else:
            x = x[3:]
            for i in x:
                if (i != '-'):
                    binaryPermissions = binaryPermissions + '1'
                else:
                    binaryPermissions = binaryPermissions + '0'
    convertBinaryToAscii()

#parses file permissions
def parseFilePermissions(x):
    tmp = x.split('\n', 1)[0] #splits on new lines and takes the first. Not neccessary with this library but I leave it there. It cant hurt anything.
    tmp = x.split(' ', 1)[0]# splits on spaces and takes the first. this gets rid of everything except for the permissions.
    filePermissions.append(tmp) # adds permissions to global string
    

#Establish FTP Connection using convenient library
ftp = FTP('www.jeangourd.com')
ftp.login()
ftp.cwd('~/7')
ftp.retrlines('LIST', parseFilePermissions) #get a list of the files 

time.sleep(1) #wait some time may need to increase
convertPermissionsToBinary()