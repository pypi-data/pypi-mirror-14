#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			November 2008
"""
from __future__ import with_statement
import cherrypy
from ZODB.POSException import ConflictError
from cocktail.events import event_handler, when
from cocktail.schema import (
    Adapter, ErrorList, DictAccessor, Collection, Reference
)
from cocktail.translations import translations
from cocktail.persistence import datastore
from cocktail.controllers import request_property, get_parameter
from woost.models import (
    Configuration,
    changeset_context,
    ChangeSet,
    get_current_user,
    restricted_modification_context,
    delete_validating,
    ReadTranslationPermission
)
from woost.controllers.backoffice.editstack import RelationNode, EditNode
from woost.controllers.backoffice.useractions import get_user_action
from woost.controllers.backoffice.basebackofficecontroller \
        import BaseBackOfficeController


class EditController(BaseBackOfficeController):

    MAX_TRANSACTION_ATTEMPTS = 3
    section = None

    @event_handler
    def handle_processed(cls, event):
        controller = event.source
        controller.context["parent_handler"].section_redirection()
        controller.stack_node.section = controller.section

    @request_property
    def errors(self):
        if self.action:
            return ErrorList(self.action.get_errors(self, self.action_selection))
        else:
            return []

    @request_property
    def available_languages(self):
        user = get_current_user()
        return [language
                for language in Configuration.instance.languages
                if user.has_permission(
                    ReadTranslationPermission,
                    language = language
                )]

    @request_property
    def action(self):
        return self._get_user_action("item_action")

    @request_property
    def action_selection(self):
        return [self.stack_node.item]

    @request_property
    def relation_action(self):
        return self._relation_action_data[0]

    @request_property
    def relation_member(self):
        return self._relation_action_data[1]

    @request_property
    def _relation_action_data(self):
        for key, value in cherrypy.request.params.iteritems():
            if key.startswith("relation_action-"):
                member_name = key.split("-", 1)[1]

                action = get_user_action(value)
                if action and not action.enabled:
                    action = None

                member = self.stack_node.content_type.get_member(member_name)
                if not isinstance(member, (Collection, Reference)):
                    member = None

                return action, member

        return None, None

    @request_property
    def relation_selection(self):
        member = self.relation_member
        value = get_parameter(
            Collection(
                name = "relation_selection-" + member.name,
                items = Reference(type = member.related_type)
            )
        )
        if not value:
            return []
        else:
            enum = frozenset(self.stack_node.form_data.get(member.name))
            return [item for item in value if item in enum]

    @request_property
    def submitted(self):
        return self.action or self.relation_action

    @request_property
    def ready(self):
        return self.submitted and not self.errors

    def submit(self):
        if self.action:
            self._invoke_user_action(
                self.action,
                self.action_selection
            )
        elif self.relation_action:
            self._invoke_user_action(
                self.relation_action,
                self.relation_selection
            )

    def save_item(self, close = False):

        for i in range(self.MAX_TRANSACTION_ATTEMPTS):
            user = get_current_user()
            stack_node = self.stack_node
            item = stack_node.item
            is_new = not item.is_inserted
            changeset = None

            with restricted_modification_context(
                item,
                user,
                member_subset = set(stack_node.form_schema.members())
            ):
                with changeset_context(author = user) as changeset:
                    self._apply_changes(item)
            try:
                datastore.commit()
            except ConflictError:
                datastore.abort()
                datastore.sync()
            else:
                break

        change = changeset.changes.get(item.id) if changeset else None

        # Creating a new nested object: relate the created item to its owner
        if is_new and isinstance(stack_node.parent_node, RelationNode):
            member = stack_node.parent_node.member
            parent_edit_node = stack_node.get_ancestor_node(EditNode)
            parent_edit_node.relate(member, item)

        # User notification
        stack_node.item_saved_notification(is_new, change)

        # Edit stack event
        stack_node.committed(
            user = user,
            changeset = changeset
        )

        # Application-wide event
        if change is not None:
            self.context["cms"].item_saved(
                item = item,
                user = user,
                is_new = is_new,
                change = change
            )

        # Close the current node, or redirect to it using a GET request (to
        # prevent double posts)
        if close:
            self.go_back()
        else:
            raise cherrypy.HTTPRedirect(self.edit_uri(item))

    def _apply_changes(self, item):

        # Remove those instances that have been dettached from an integral
        # reference
        @when(item.changed)
        def delete_replaced_integral_children(event):
            if isinstance(event.member, Reference) \
            and event.member.integral \
            and event.previous_value is not None:
                delete_validating(event.previous_value)

        try:
            stack_node = self.stack_node
            stack_node.import_form_data(stack_node.form_data, item)
            item.insert()
            stack_node.saving(
                user = get_current_user(),
                changeset = ChangeSet.current
            )
        finally:
            item.changed.remove(delete_replaced_integral_children)

    @request_property
    def tab(self):
        return cherrypy.request.params.get("tab")

    @request_property
    def output(self):
        output = BaseBackOfficeController.output(self)
        stack_node = self.stack_node
        output.update(
            edited_item = stack_node.item,
            edited_content_type = stack_node.content_type,
            errors = self.errors,
            form_schema = stack_node.form_schema,
            form_data = stack_node.form_data,
            changes = set(stack_node.iter_changes()),
            item_translations = stack_node.item_translations,
            visible_translations = stack_node.visible_translations,
            section = self.section,
            tab = self.tab
        )
        return output

