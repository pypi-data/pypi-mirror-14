#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from warnings import warn
from woost import app

def get_current_website():
    """Gets the active website for the present context.

    The concept of an 'active' website is used by the publication machinery to
    limit the availability of content based on the site that is being visited.

    @rtype: L{Website}
    """
    warn(
        "get_current_website() has been deprecated; use app.website instead",
        DeprecationWarning,
        stacklevel = 2
    )
    return app.website

def set_current_website(website):
    """Sets the active website for the present context. See
    L{get_current_website} for more information.

    @param website: The website to set as active.
    @type website: L{Website}
    """
    warn(
        "set_current_website() has been deprecated; use app.website instead",
        DeprecationWarning,
        stacklevel = 2
    )
    app.website = website

