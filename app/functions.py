#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os

#cryptage des données
def crypted_string(string):
    """
    Fonction permettant de crypter une chaine de caractère avec le protocole sha1.
    La fonction retourne un nombre hexadécimal au format str.
    """
    b_string=string.encode() 
    crypted_str=hashlib.sha1(b_string) 
    return crypted_str.hexdigest()
