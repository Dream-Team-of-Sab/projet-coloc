#!/bin/bash
isExistApp=`pgrep httpd`
if [[ -n  $isExistApp ]]; then
    service httpd stop 
fi
isExistApp=`pgrep mariadb`
if [[ -n  $isExistApp ]]; then
    service mariadb stop 
fi
