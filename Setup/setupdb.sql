CREATE USER 'jgourd'@'%' IDENTIFIED BY 'gourd';
GRANT select on * . * to 'jgourd'@'%';
FLUSH PRIVILEGES;

CREATE DATABASE canes_venatici;
