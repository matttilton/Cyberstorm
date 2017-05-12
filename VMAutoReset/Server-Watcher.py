import urllib2
import time
import subprocess
import telnetlib
import os
import pty
import ftplib

class ssh():
    def __init__(self, host, execute='echo "done" > /root/testing.txt', 
                 askpass=False, user='jgourd3', password=b'jgourd3'):
        self.exec_ = execute
        self.host = host
        self.user = user
        self.password = password
        self.askpass = askpass
        self.run()

    def run(self):
        command = [
                '/usr/bin/ssh',
                self.user+'@'+self.host,
                '-o', 'NumberOfPasswordPrompts=1',
                self.exec_,
        ]

        # PID = 0 for child, and the PID of the child for the parent    
        pid, child_fd = pty.fork()

        if not pid: # Child process
            # Replace child process with our SSH process
            os.execv(command[0], command)

        ## if we havn't setup pub-key authentication
        ## we can loop for a password promt and "insert" the password.
        while self.askpass:
            try:
                output = os.read(child_fd, 1024).strip()
            except:
                break
            lower = output.lower()
            # Write the password
            if b'password:' in lower:
                os.write(child_fd, self.password + b'\n')
                break
            elif b'are you sure you want to continue connecting' in lower:
                # Adding key to known_hosts
                os.write(child_fd, b'yes\n')
            else:
                print('Error:',output)

        # See if there's more output to read after the password has been sent,
        # And capture it in a list.
        output = []
        while True:
            try:
                output.append(os.read(child_fd, 1024).strip())
            except:
                break

        os.waitpid(pid, 0)
        return ''.join(output)

while(1):

    # html test
    html_response = urllib2.urlopen('http://127.0.0.1:80')
    html_source = html_response.read()

    if 'Canes Venatici' in html_source:
        print 'apache is fine'
    else:
        server = telnetlib.Telnet(config["host"], config["port"], config["timeout"])
        server.write('reset ' + str(config["name"]) + ' ' + str(config["watchlist"][num]))
        server.close()
    
    # ssh test
    s = ssh("127.0.0.1", execute='', askpass=True)
    ssh_result = s.run()

    if 'Canes Venatici' in ssh_result:
        print 'ssh is fine'
    else:
        server = telnetlib.Telnet(config["host"], config["port"], config["timeout"])
        server.write('reset ' + str(config["name"]) + ' ' + str(config["watchlist"][num]))
        server.close()
    
    # ftp test
    ftp = ftplib.FTP('localhost')
    ftp_result = ftp.getwelcome()
    if 'Canes Venatici' in ftp_result:
        print 'ftp is fine'
    else:
        server = telnetlib.Telnet(config["host"], config["port"], config["timeout"])
        server.write('reset ' + str(config["name"]) + ' ' + str(config["watchlist"][num]))
        server.close()
    
    # mysql test

    time.sleep(1)

