#!/home/kaitoshinomiya/.pyenv/versions/3.7.11/bin/python
# -*- coding: utf-8 -*-
import cgitb
cgitb.enable()

from wsgiref.handlers import CGIHandler
from app import app

CGIHandler().run(app)
