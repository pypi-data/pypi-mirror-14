#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail.html import Element, templates
from woost.models import Publishable, News
from woost.views.viewfactory import ViewFactory

# Text only
#------------------------------------------------------------------------------
text_only = ViewFactory()

@text_only.handler_for(Publishable)
def item_link(item, parameters):
    view = Element("a")
    view["href"] = item.get_uri()
    view.append(translations(item))
    return view

# Text and icons
#------------------------------------------------------------------------------
text_and_icon = ViewFactory()

@text_and_icon.handler_for(Publishable)
def item_link_with_icon(item, parameters):

    view = templates.new(
        "woost.extensions.newsletters.NewsletterTextAndIconLink"
    )
    view.item = item

    image_factory = parameters.get("image_factory")
    if image_factory is None:
        view.image_factory = image_factory

    return view

# Summary
#------------------------------------------------------------------------------
summary = ViewFactory()

@summary.handler_for(News)
def news_summary(news, parameters):

    view = templates.new(
        "woost.extensions.newsletters.NewsletterNewsSummary"
    )
    view.news = news

    image_factory = parameters.get("image_factory")
    if image_factory is None:
        view.image_factory = image_factory

    return view

summary.register(Publishable, "item_link", item_link)

