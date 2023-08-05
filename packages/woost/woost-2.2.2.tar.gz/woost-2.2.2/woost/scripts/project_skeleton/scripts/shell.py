#!/usr/bin/env python
#-*- coding: utf-8 -*-
u"""A convenience script that can be launched through ipython or vanilla python
with the -i flag, to have quick access to the project's data.
"""
from woost.scripts.shell import *
from _PROJECT_MODULE_.models import *
setup_shell(locals())

