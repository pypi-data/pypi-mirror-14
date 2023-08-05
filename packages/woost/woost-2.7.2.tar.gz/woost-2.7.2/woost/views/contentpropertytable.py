#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			February 2009
"""
from cocktail.html import templates
from woost.views.uigeneration import backoffice_display

PropertyTable = templates.get_class("cocktail.html.PropertyTable")


class ContentPropertyTable(PropertyTable):

    base_ui_generators = [backoffice_display]

