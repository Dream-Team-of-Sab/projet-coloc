#!/bin/bash
sudo yum update
sudo amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
sudo yum install -y mariadb-server mariadb httpd php-xml php-mbstring
php -r "readfile('https://getcomposer.org/installer');"|php -- --install-dir=/usr/local/bin
chmod +x /usr/local/bin/composer.phar
