#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
import webbrowser
from cocktail.translations import *
from cocktail.persistence import *
from woost import app
from woost.models import *
from woost.models.utils import *
from woost.models.extension import load_extensions

def setup_shell(env):
    env["config"] = config = Configuration.instance
    config.setup_languages()
    set_current_user(User.require_instance(qname = "woost.anonymous_user"))
    set_current_website(config.websites[0])
    load_extensions()

get = Item.get_instance
req = Item.require_instance

def show(target):

    if isinstance(target, Publishable):
        webbrowser.open(target.get_uri(host = "!"))
    elif hasattr(target, "__iter__"):
        for item in target:
            show(item)
    else:
        print "Can't show non-publishable object %r" % target

def edit(target):

    backoffice = Publishable.require_instance(qname = "woost.backoffice")

    if isinstance(target, Item):
        webbrowser.open(
            backoffice.get_uri(
                host = "!",
                path = ["content", str(target.id)]
            )
        )
    elif hasattr(target, "__iter__"):
        for item in target:
            edit(item)
    else:
        print "Can't edit object %r" % target

