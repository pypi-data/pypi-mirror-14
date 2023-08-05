#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from threading import local

_thread_data = local()

def get_current_website():
    """Gets the active website for the present context.

    The concept of an 'active' website is used by the publication machinery to
    limit the availability of content based on the site that is being visited.

    @rtype: L{Website}
    """
    return getattr(_thread_data, "website", None)

def set_current_website(website):
    """Sets the active website for the present context. See
    L{get_current_website} for more information.

    @param website: The website to set as active.
    @type website: L{Website}
    """
    _thread_data.website = website

