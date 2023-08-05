#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			July 2008
"""
from warnings import warn
warn(
    "woost.controllers.language.LanguageModule is deprecated, "
    "use woost.languagescheme.LanguageScheme instead "
    "(or its global instance through woost.app.language)",
    DeprecationWarning
)

from woost.languagescheme import LanguageScheme as LanguageModule

