#!/bin/bash
#
# --------------------------------------------------------------------
# This is a free shell script under GNU GPL version 3.0 or above
# Copyright (C) 2005 ReFlectiv project.
# Feedback/comment/suggestions : http://www.reflectiv.net/
# -------------------------------------------------------------------------
#
# This script automatically set up a new *Debian* server (IMPORTANT : Debian!), by doing these actions :
#
# * Modification of the root password
# * Creating users
# * Securing SSH
# * Install and set some security for :
# ** Apache
# *** Disable modules : userdir suexec cgi cgid dav include autoindex authn_file status env headers proxy proxy_balancer proxy_http headers
# *** Enable modules : expires rewrite setenvif ssl
# ** Mysql
# *** Execute mysql_secure_installation script
#
# @see http://plusbryan.com/my-first-5-minutes-on-a-server-or-essential-security-for-linux-servers
# For install NGinx & PHP, see :
# @see https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-on-debian-7

# First of all, we check if the user is root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# Changing the password of the root user
read -e -p "Do you want to change the root password? [Y/n] : " change_password
if [[ ("$change_password" == "y" || "$change_password" == "Y" || "$change_password" == "") ]]; then
    passwd
fi

# Creating multiple users
create_user=true
read -e -p "Create group sshusers? [Y/n] : " create_sshusers
if [[ ("$create_sshusers" == "y" || "$create_sshusers" == "Y" || "$create_sshusers" == "") ]]; then
    groupadd sshusers
fi

while $create_user; do
    read -e -p "Create a new user? [y/N] : " new_user

    if [[ ("$new_user" == "y" || "$new_user" == "Y") ]]; then
        read -e -p "Username : " user_name
        adduser $user_name
        adduser $user_name sshusers
    else
        create_user=false
    fi
done


# SSH Server
echo "Improving security on SSH"

echo " * Disallow X11Forwarding"
sed -i "s/X11Forwarding yes/X11Forwarding no/" /etc/ssh/sshd_config

echo " * Removing Root Login"
sed -i "s/PermitRootLogin yes/PermitRootLogin no/" /etc/ssh/sshd_config

if grep -q -e 'UseDNS' /etc/ssh/sshd_config
    then echo "UseDns already present"
    else echo "UseDNS no" >> /etc/ssh/sshd_config
fi

echo "This server is owned by Canes Venatici. Goodbye." >> /etc/motd

read -e -p "SSH Allowed users (space separated) : " ssh_users
if [[ $ssh_users ]]; then
    echo "AllowUsers $ssh_users" >> /etc/ssh/sshd_config
fi

read -e -p "Setup jail? [Y/n] : " jail
if [[ ("$jail" == "y" || "$jail" == "Y" || "$jail" == "") ]]; then
    mkdir -p /var/jail/{dev,etc,lib,usr,bin}
    mkdir -p /var/jail/usr/bin
    chown root.root /var/jail
    mknod -m 666 /var/jail/dev/null c 1 3
    cp /etc/ld.so.cache /var/jail/etc
    cp /etc/ld.so.conf /var/jail/etc
    cp /etc/nsswitch.conf /var/jail/etc
    cp /etc/hosts /var/jail/etc
    cp /bin/bash /var/jail/bin/
    if grep -q -e 'Match group sshusers' /etc/ssh/sshd_config
        then echo 'already have jail'
        else echo "Match group sshusers
          ChrootDirectory /var/jail/
          X11Forwarding no
          AllowTcpForwarding no" >> /etc/ssh/sshd_config
    fi
fi


/etc/init.d/ssh restart

read -e -p "Setup Apache? [Y/n] : " setup_apache
if [[ ("$setup_apache" == "y" || "$setup_apache" == "Y" || "$setup_apache" == "") ]]; then
    a2dismod userdir suexec cgi cgid dav include autoindex authn_file status env headers proxy proxy_balancer proxy_http headers 
    a2enmod expires rewrite setenvif ssl
    cp index.html /var/www/html/index.html

    /etc/init.d/apache2 restart
fi

read -e -p "Setup Vsftpd? [Y/n] : " setup_vsftpd
if [[ ("$setup_vsftpd" == "y" || "$setup_vsftpd" == "Y" || "$setup_vsftpd" == "") ]]; then
    sed -i "s/anonymous_enable=NO/anonymous_enable=YES/" /etc/vsftpd.conf
    sed -i "s/local_enable=YES/local_enable=NO/" /etc/vsftpd.conf
    sed -i 's/.*ftpd_banner=.*/ftpd_banner=This ftp server belongs to Canes Venatici/' /etc/vsftpd.conf
    mkdir /home/ftp
    echo "anon_root=/home/ftp" >> /etc/vsftpd.conf

    service vsftpd restart
fi

read -e -p "Setup MySQL? [Y/n] : " install_mysql
if [[ ("$install_mysql" == "y" || "$install_mysql" == "Y" || "$install_mysql" == "") ]]; then

    read -e -p "Execute mysql_secure_installation ? [Y/n] : " mysql_secure
    if [[ ("$mysql_secure" == "y" || "$mysql_secure" == "Y" || "$mysql_secure" == "") ]]; then
        mysql_secure_installation
    fi
    echo "Input mysql root password"
    mysql -uroot -p < setupdb.sql
fi

exit 0;