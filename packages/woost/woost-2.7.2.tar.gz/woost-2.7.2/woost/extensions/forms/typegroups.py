#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost.models import type_groups, TypeGroup

type_groups["setup"].append(
    TypeGroup("custom_forms")
)

