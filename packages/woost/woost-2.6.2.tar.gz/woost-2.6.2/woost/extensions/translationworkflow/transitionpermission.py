#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from woost.models.messagestyles import permission_doesnt_match_style
from woost.models.permission import ContentPermission
from .request import TranslationWorkflowRequest
from .transition import TranslationWorkflowTransition


class TranslationWorkflowTransitionPermission(ContentPermission):

    transitions = schema.Collection(
        items = schema.Reference(
            type = TranslationWorkflowTransition
        ),
        related_end = schema.Collection(),
        after_member = "content_expression"
    )

    def match(
        self,
        user,
        transition,
        translation_request = None,
        verbose = False
    ):
        if not ContentPermission.match(
            self,
            user,
            TranslationWorkflowRequest
                if translation_request is None
                else translation_request.translated_item,
            verbose = verbose
        ):
            return False

        if self.transitions and transition not in self.transitions:
            if verbose:
                print permission_doesnt_match_style(
                    "transition doesn't match"
                )
            return False

        return True

