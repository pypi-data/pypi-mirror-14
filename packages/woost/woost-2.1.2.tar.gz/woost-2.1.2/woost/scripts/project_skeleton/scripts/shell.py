#!/usr/bin/env python
#-*- coding: utf-8 -*-
u"""A convenience script that can be launched through ipython or vanilla python
with the -i flag, to have quick access to the project's data.
"""
from __future__ import with_statement
from cocktail.translations import *
from cocktail.persistence import *
from woost import app
from woost.models import *
from woost.models.extension import load_extensions
from _PROJECT_MODULE_.models import *

config = Configuration.instance
config.setup_languages()
set_current_user(User.require_instance(qname = "woost.anonymous_user"))
set_current_website(config.websites[0])

load_extensions()

