#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.modeling import extend, call_base
from cocktail.translations import translations
from cocktail import schema
from cocktail.html.datadisplay import display_factory
from woost.models import Publishable

Publishable.add_member(
    schema.Reference("access_restriction",
        type = "woost.extensions.restrictedaccess.accessrestriction."
               "AccessRestriction",
        bidirectional = True,
        indexed = True,
        listed_by_default = False,
        edit_control = display_factory(
            "cocktail.html.RadioSelector",
            empty_option_displayed = True
        ),
        search_control = "cocktail.html.DropdownSelector",
        member_group = "publication"
    )
)

@extend(Publishable.access_restriction)
def translate_value(self, value, language = None, **kwargs):

    if not value:
        return translations(
            "Publishable.access_restriction=None",
            language,
            **kwargs
        )

    return call_base(value, language, **kwargs)

