#-*- coding: utf-8 -*-
"""

@author:		Jordi Fernández
@contact:		jordi.fernandez@whads.com
@organization:	Whads/Accent SL
@since:			September 2010
"""
from cocktail import schema
from woost.models import Permission
from woost.models.messagestyles import permission_doesnt_match_style
from woost.extensions.mailer.mailinglist import MailingList


class SendEmailPermission(Permission):
    """Permission to send an email."""

    instantiable = True

    lists = schema.Collection(
        items = schema.Reference(
            type = MailingList,
        ),
        related_end = schema.Collection(),
        edit_control = "cocktail.html.CheckList"
    )

    def match(self, user, mailingList = None, verbose = False):

        if mailingList and self.lists and mailingList not in self.lists:

            if verbose:
                print permission_doesnt_match_style("Mailing list doesn't match")

            return False

        return Permission.match(self, user, verbose)

