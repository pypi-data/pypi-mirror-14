#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			July 2008
"""
import cherrypy
from cocktail import schema
from cocktail.events import event_handler
from cocktail.html import templates
from .publishable import Publishable
from .controller import Controller


class Document(Publishable):

    instantiable = True
    type_group = "document"
    default_per_language_publication = True

    groups_order = [
        "content", "navigation", "presentation", "publication", "meta",
        "robots"
    ]

    members_order = (
        "title",
        "inner_title",
        "template",
        "description",
        "keywords",
        "children",
        "redirection_mode",
        "redirection_target",
        "redirection_method",
        "robots_should_index",
        "robots_should_follow"
    )

    default_controller = schema.DynamicDefault(
        lambda: Controller.get_instance(qname = "woost.document_controller")
    )

    title = schema.String(
        indexed = True,
        normalized_index = True,
        full_text_indexed = True,
        descriptive = True,
        translated = True,
        required = True,
        member_group = "content"
    )

    inner_title = schema.String(
        translated = True,
        listed_by_default = False,
        member_group = "content"
    )

    description = schema.String(
        translated = True,
        listed_by_default = False,
        edit_control = "cocktail.html.TextArea",
        member_group = "meta"
    )

    keywords = schema.String(
        translated = True,
        listed_by_default = False,
        edit_control = "cocktail.html.TextArea",
        member_group = "meta"
    )

    template = schema.Reference(
        type = "woost.models.Template",
        bidirectional = True,
        listed_by_default = False,
        after_member = "controller",
        member_group = "presentation.behavior"
    )

    children = schema.Collection(
        items = "woost.models.Publishable",
        bidirectional = True,
        related_key = "parent",
        cascade_delete = True,
        after_member = "parent",
        member_group = "navigation"
    )

    redirection_mode = schema.String(
        enumeration = ["first_child", "custom_target"],
        listed_by_default = False,
        text_search = False,
        member_group = "navigation"
    )

    redirection_target = schema.Reference(
        type = Publishable,
        related_end = schema.Collection(),
        required = redirection_mode.equal("custom_target"),
        listed_by_default = False,
        member_group = "navigation"
    )

    redirection_method = schema.String(
        required = True,
        default = "temp",
        enumeration = ["temp", "perm", "client"],
        listed_by_default = False,
        text_search = False,
        member_group = "navigation"
    )

    robots_should_index = schema.Boolean(
        required = True,
        default = True,
        listed_by_default = False,
        member_group = "meta.robots"
    )

    robots_should_follow = schema.Boolean(
        required = True,
        default = True,
        listed_by_default = False,
        member_group = "meta.robots"
    )

    def _update_path(self, parent, path):

        Publishable._update_path(self, parent, path)

        if self.children:
            for child in self.children:
                child._update_path(self, child.path)

    def descend_tree(self, include_self = False):

        if include_self:
            yield self

        if self.children:
            for child in self.children:
                for descendant in child.descend_tree(True):
                    yield descendant

    def render(self, **values):
        """Renders the document using its template."""
        if self.template is None:
            raise ValueError("Can't render a document without a template")

        values["publishable"] = self

        view = templates.new(self.template.identifier)
        for key, value in values.iteritems():
            setattr(view, key, value)

        return view.render_page()

    def find_redirection_target(self):
        mode = self.redirection_mode

        if mode == "first_child":
            return self.find_first_child_redirection_target()

        elif mode == "custom_target":
            return self.redirection_target

    def find_first_child_redirection_target(self):
        for child in self.children:
            if child.is_accessible():
                if isinstance(child, Document):
                    return child.find_redirection_target() or child
                else:
                    return child

    def first_child_redirection(self):
        child = self.find_first_child_redirection_target()
        if child is not None:
            raise cherrypy.HTTPRedirect(child.get_uri())

    @event_handler
    def handle_related(cls, event):
        if event.member is cls.websites:
            for child in event.source.children:
                child.websites = list(event.source.websites)

    @event_handler
    def handle_unrelated(cls, event):
        if not event.source.is_deleted:
            if event.member is cls.websites:
                for child in event.source.children:
                    child.websites = list(event.source.websites)


