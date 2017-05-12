#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

read -e -p "Change Apache? [Y/n] : " change_apache
if [[ ("$change_apache" == "y" || "$change_apache" == "Y" || "$change_apache" == "") ]]; then
    read -e -p "New Port : " new_apache
    sed -i "s/Listen .*/Listen $new_apache/" /etc/apache2/ports.conf
    sed -i "s/<VirtualHost .*/<VirtualHost *:$new_apache>/" /etc/apache2/sites-enabled/000-default.conf
    /etc/init.d/apache2 restart
fi

read -e -p "Change FTP? [Y/n] : " change_ftp
if [[ ("$change_ftp" == "y" || "$change_ftp" == "Y" || "$change_ftp" == "") ]]; then
    read -e -p "New Port : " new_ftp
    if grep -q -e 'connect_from_port_20=YES' /etc/vsftpd.conf
        then sed -i "s/connect_from_port_20=YES/#connect_from_port_20=YES/" /etc/vsftpd.conf
    fi
    if grep -q -e 'listen_port' /etc/vsftpd.conf
        then sed -i "s/listen_port=.*/listen_port=$new_ftp/" /etc/vsftpd.conf
        else echo "listen_port=$new_ftp" >> /etc/vsftpd.conf
    fi
    
    service vsftpd restart
fi

read -e -p "Change SSH? [Y/n] : " change_ssh
if [[ ("$change_ssh" == "y" || "$change_ssh" == "Y" || "$change_ssh" == "") ]]; then
    read -e -p "New Port : " new_ssh
    sed -i "s/Port .*/Port $new_ssh/" /etc/ssh/sshd_config
    /etc/init.d/ssh restart
fi