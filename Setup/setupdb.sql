CREATE LOGIN 'jgourd'@'%' IDENTIFIED BY 'gourdscheezyjalapenosoup';
GRANT select on * . * to 'jgourd'@'%';
FLUSH PRIVILEGES;

CREATE DATABASE canes_venatici;