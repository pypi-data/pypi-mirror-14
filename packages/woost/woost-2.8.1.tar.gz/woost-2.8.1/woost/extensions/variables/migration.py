#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.events import when
from cocktail.persistence import MigrationStep

step = MigrationStep(
    "woost.extensions.variables: Rename Variable.expression to .dynamic_value"
)

@when(step.executing)
def rename_variable_expression_member(e):

    from woost.extensions.variables.variable import Variable

    for variable in Variable.select():
        try:
            value = variable._expression
        except AttributeError:
            continue
        else:
            del variable._expression
            variable.dynamic_value = value

