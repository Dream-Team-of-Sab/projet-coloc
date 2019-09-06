#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'app/templates/uploads'

#cryptage des données
def crypted_string(string):
    """
    Fonction permettant de crypter une chaine de caractère avec le protocole sha1.
    La fonction retourne un nombre hexadécimal au format str.
    """
    b_string=string.encode() 
    crypted_str=hashlib.sha1(b_string) 
    return crypted_str.hexdigest()

# Index view
def allowed_file(filename):
    """
    Récupère puis vérifie que l'extension est bien
    dans la liste des extensions autorisées
    """
    if '.' in filename and filename.split('.')[-1] in ALLOWED_EXTENSIONS: 
        return True 
    else: 
        return False  

def upload_file(up_file, invoice_id):
    """
    Fonction permettant d'uploader une photo de la facturette
    d'un utilisateur
    """
    file_name = up_file.filename
    if allowed_file(file_name):
        file_name = str(invoice_id) + '.' + file_name.split('.')[-1]
        up_file.save(os.path.join(UPLOAD_FOLDER, file_name))
