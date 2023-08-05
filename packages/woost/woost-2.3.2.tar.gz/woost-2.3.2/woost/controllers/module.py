#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			July 2008
"""
from warnings import warn
warn(
    "woost.controllers.module.Module is deprecated, and its subclasses "
    "(LanguageModule and AuthenticationModule) have been relocated to "
    "woost.app",
    DeprecationWarning
)


class Module(object):

    def __init__(self, application):
        self.application = application

