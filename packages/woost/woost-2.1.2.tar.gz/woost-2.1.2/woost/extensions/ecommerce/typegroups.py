#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Jordi Fernández <jordi.fernandez@whads.com>
"""
from woost.models import type_groups, block_type_groups, TypeGroup


type_groups["setup"].append(TypeGroup("ecommerce"))

block_type_groups.append(TypeGroup("blocks.ecommerce"))
