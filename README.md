HOW TO USE THE PROGRAMS - WALDEN

= = binary_decoder.py = = = = = = = = 
$ touch binary.txt
binary.txt should be the binary code with no whitespace

$ python binary_decoder.py < binary.txt
 
 = = = = = = = = = = chat_client.py = = = = = = = = = = =
Change the first few varibles 
ip
port
ONE -> time middle point between sessions

if he changes the way the mechanics work edit the main loop


$ python chat_client.py
 = = = = = = = = = = = = ftp.py = = = = = = = = = = = = =
edit config varibles at the bottom of the file
$ python ftp.py


 = = = = = = = = = = Timelock.py = = = = = = = = = = = = =

$ touch epoch
epoch file should be the epoch time in "YYYY MM DD HH mm SS"

Change Line 70:
    current_time = "2017 05 04 12 57 34" 
to the time you want with "YYYY MM DD HH mm SS"

$ python Timelock.py < epoch
    

 = = = = = = = = = = = vigenere.py = = = = = = = = = = = = =
$ touch cipher
cipher should be text to be processed by vigenere

$ python vigenere.py [-d|-e] [key] < cipher

 = = = = = = = = = = = = = xor.py = = = = = = = = = = = = = 
$ touch key
key file should contain the key used in xoring

$ python xor.py < plaintext > ciphertext
$ python xor.py < ciphertext
