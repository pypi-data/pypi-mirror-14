#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			July 2008
"""
from warnings import warn
warn(
    "woost.controllers.authentication.AuthenticationModule is deprecated, "
    "use woost.authenticationscheme.AuthenticationScheme instead "
    "(or its global instance through woost.app.authentication)",
    DeprecationWarning
)

from woost.authenticationscheme import (
    AuthenticationScheme as AuthenticationModule,
    AuthenticationFailedError
)

