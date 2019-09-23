#!/bin/bash
cd /var/www/html/laravel
sudo composer install
chmod -R 777 /var/www/html/laravel
rm /etc/httpd/conf.d/welcome.conf
cp /var/www/html/laravel/scripts/laravel.conf /etc/httpd/conf.d/welcome.conf
