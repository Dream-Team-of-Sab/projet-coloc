#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)
app.secret_key = 'bc7466e0f98a79cee6389aac5130e2fe4b75e03e'

from app import routes
