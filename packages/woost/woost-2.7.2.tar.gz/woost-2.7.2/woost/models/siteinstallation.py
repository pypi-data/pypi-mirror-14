#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			November 2013
"""
from cocktail.events import event_handler
from cocktail import schema
from .item import Item
from .user import User


class SiteInstallation(Item):

    type_group = "setup"
    edit_form = "woost.views.SiteInstallationForm"

    edit_node_class = (
        "woost.controllers.backoffice."
        "siteinstallationeditnode.SiteInstallationEditNode"
    )

    members_order = (
        "title",
        "url",
        "synchronization_user",
        "synchronization_password"
    )

    default_synchronizable = False

    title = schema.String(
        indexed = True,
        unique = True,
        descriptive = True,
        required = True,
        spellcheck = True
    )

    url = schema.URL(
        required = True
    )

    synchronization_user = schema.String(
        listed_by_default = False
    )

    synchronization_password = schema.String(
        listed = False,
        listed_by_default = False,
        visible_in_detail_view = False,
        searchable = False,
        text_search = False,
        edit_control = "cocktail.html.PasswordBox"
    )

    @event_handler
    def handle_changing(cls, event):

        if event.member is cls.synchronization_password \
        and event.value is not None:
            event.value = User.encryption(event.value)

    def test_password(self, password):
        """Indicates if the user's password matches the given string.

        @param password: An unencrypted string to tests against the user's
            encrypted password.
        @type password: str

        @return: True if the passwords match, False otherwise.
        @rtype: bool
        """
        if password:
            return self.encryption(password) == self.synchronization_password
        else:
            return not self.synchronization_password

