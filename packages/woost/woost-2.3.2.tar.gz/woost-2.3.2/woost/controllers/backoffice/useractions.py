#-*- coding: utf-8 -*-
u"""
Declaration of back office actions.

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			December 2008
"""
import cherrypy
from cocktail.modeling import getter, ListWrapper
from cocktail.translations import translations
from cocktail.persistence import datastore
from cocktail.controllers import (
    view_state,
    Location,
    context as controller_context,
    request_property,
    get_parameter,
    session,
)
from cocktail import schema
from woost.models import (
    Configuration,
    Item,
    SiteInstallation,
    Publishable,
    URI,
    File,
    Block,
    get_current_user,
    ReadPermission,
    ReadMemberPermission,
    CreatePermission,
    ModifyPermission,
    DeletePermission,
    ModifyMemberPermission,
    ReadHistoryPermission,
    InstallationSyncPermission
)
from woost.models.blockutils import add_block, type_is_block_container
from woost.controllers.notifications import notify_user
from woost.controllers.backoffice.editstack import (
    EditNode,
    SelectionNode,
    RelationNode,
    EditBlocksNode,
    AddBlockNode
)

# User action model declaration
#------------------------------------------------------------------------------

# Class stub (needed by the metaclass)
UserAction = None

_action_list = ListWrapper([])
_action_map = {}

def get_user_action(id):
    """Gets a user action, given its unique identifier.

    @param id: The unique identifier of the action to obtain.
    @type id: str

    @return: The requested user action, or None if not defined.
    @rtype: L{UserAction}
    """
    return _action_map.get(id)

def get_user_actions(**kwargs):
    """Returns a collection of all actions registered with the site.

    @return: The list of user actions.
    @rtype: iterable L{UserAction} sequence
    """
    return _action_list

def get_view_actions(context, target = None):
    """Obtains the list of actions that can be displayed on a given view.

    @param context: A set of string identifiers, such as "context_menu",
        "toolbar", etc. Different views can make use of as many different
        identifiers as they require.
    @type container: str set

    @param target: The item or content type affected by the action.
    @type target: L{Item<woost.models.item.Item>} instance or class

    @return: The list of user actions available under the specified context.
    @rtype: iterable L{UserAction} sequence
    """
    return (
        action
        for action in _action_list
        if action.enabled
            and action.is_available(context, target)
    )

def add_view_action_context(view, clue):
    """Adds contextual information to the given view, to be gathered by
    L{get_view_actions_context} and passed to L{get_view_actions}.

    @param view: The view that gains the context clue.
    @type view: L{Element<cocktail.html.element.Element>}

    @param clue: The context identifier added to the view.
    @type clue: str
    """
    view_context = getattr(view, "actions_context", None)
    if view_context is None:
        view_context = set()
        view.actions_context = view_context
    view_context.add(clue)

def get_view_actions_context(view):
    """Extracts clues on the context that applies to a given view and its
    ancestors, to supply to the L{get_view_actions} function.

    @param view: The view to inspect.
    @type view: L{Element<cocktail.html.element.Element>}

    @return: The set of context identifiers for the view and its ancestors.
    @rtype: str set
    """
    context = set()

    while view:
        view_context = getattr(view, "actions_context", None)
        if view_context:
            context.update(view_context)
        view = view.parent

    return context


class UserAction(object):
    """An action that is made available to users at the backoffice
    interface. The user actions model allows site implementors to extend the
    site with their own actions, or to disable or override standard actions
    with fine grained control of their context.

    @ivar enabled: Controls the site-wide availavility of the action.
    @type enabled: bool

    @ivar included: A set of context identifiers under which the action is
        made available. Entries on the sequence are joined using a logical OR.
        Entries can also consist of a tuple of identifiers, which will be
        joined using a logical AND operation.
    @type included: set(str or tuple(str))

    @ivar excluded: A set of context identifiers under which the action won't
        be made available. Identifiers are specified using the same format used
        by the L{included} parameter. If both X{included} and X{excluded} are
        specified, both conditions will be tested, with X{excluded} carrying
        more weight.
    @type excluded: set(str or tuple(str))

    @ivar content_type: When set, the action will only be made available to the
        indicated content type or its subclasses.
    @type content_type: L{Item<woost.models.Item>} subclass

    @ivar ignores_selection: Set to True for actions that don't operate on a
        selection of content.
    @type ignores_selection: bool

    @ivar min: The minimum number of content items that the action can be
        invoked on. Setting it to 0 or None disables the constraint.
    @type min: int

    @ivar max: The maximum number of content items that the action can be
        invoked on. A value of None disables the constraint.
    @type max: int

    @ivar direct_link: Set to True for actions that can provide a direct URL
        for their execution, without requiring a form submit and redirection.
    @type direct_link: bool

    @ivar parameters: A schema describing user supplied parameters required by
        the action. When set to None, the action requires no additional input
        from the user.
    @type parameters: L{Schema<cocktail.schema.schema.Schema>}
    """
    enabled = True
    included = frozenset(["toolbar_extra", "item_buttons_extra"])
    excluded = frozenset([
        "selector",
        "calendar_content_view",
        "workflow_graph_content_view",
        "changelog"
    ])
    content_type = None
    ignores_selection = False
    min = 1
    max = 1
    direct_link = False
    client_redirect = False
    link_target = None
    parameters = None

    def __init__(self, id):

        if not id:
            raise ValueError("User actions must have an id")

        if not isinstance(id, basestring):
            raise TypeError("User action identifiers must be strings, not %s"
                            % type(id))
        self._id = id

    def __translate__(self, language, **kwargs):
        return translations("woost.actions." + self.id, language, **kwargs)

    @getter
    def id(self):
        """The unique identifier for the action.
        @type: str
        """
        return self._id

    def register(self, before = None, after = None):
        """Registers the action with the site, so that it can appear on action
        containers and be handled by controllers.

        Registering an action with an identifier already in use is allowed, and
        will override the previously registered action.

        @param before: Indicates the position for the registered action. Should
            match the identifier of an already registered action. The new
            action will be inserted immediately before the indicated action.
        @type before: str

        @param after: Indicates the position for the registered action. Should
            match the identifier of an already registered action. The new
            action will be inserted immediately after the indicated action.
        @type after: str

        @raise ValueError: Raised if both L{before} and L{after} are set.
        @raise ValueError: Raised if the position indicated by L{after} or
            L{before} can't be found.
        """
        if after and before:
            raise ValueError("Can't combine 'after' and 'before' parameters")

        prev_action = get_user_action(self._id)

        if after or before:
            if prev_action:
                _action_list._items.remove(prev_action)

            ref_action = _action_map[after or before]
            pos = _action_list.index(ref_action)

            if before:
                _action_list._items.insert(pos, self)
            else:
                _action_list._items.insert(pos + 1, self)

        elif prev_action:
            pos = _action_list.index(prev_action)
            _action_list._items[pos] = self
        else:
            _action_list._items.append(self)

        _action_map[self._id] = self

    def is_available(self, context, target):
        """Indicates if the user action is available under a certain context.

        @param context: A set of string identifiers, such as "context_menu",
            "toolbar", etc. Different views can make use of as many different
            identifiers as they require.
        @type container: str set

        @param target: The item or content type affected by the action.
        @type target: L{Item<woost.models.item.Item>} instance or class

        @return: True if the action can be shown in the given context, False
            otherwise.
        @rtype: bool
        """
        # Context filters
        def match(tokens):
            for token in tokens:
                if isinstance(token, str):
                    if token in context:
                        return True
                elif context.issuperset(token):
                    return True
            return False

        if self.included and not match(self.included):
            return False

        if self.excluded and match(self.excluded):
            return False

        # Content type filter
        if self.content_type is not None:
            if isinstance(target, type):
                if not issubclass(target, self.content_type):
                    return False
            else:
                if not isinstance(target, self.content_type):
                    return False

        # Authorization check
        return self.is_permitted(get_current_user(), target)

    def is_permitted(self, user, target):
        """Determines if the given user is allowed to execute the action.

        Subclasses should override this method in order to implement their
        access restrictions.

        @param user: The user to authorize.
        @type user: L{User<woost.models.user.User>}

        @param target: The item or content type affected by the action.
        @type target: L{Item<woost.models.item.Item>} instance or class

        @return: True if the user is granted permission, False otherwise.
        @rtype: bool
        """
        return True

    def get_dropdown_panel(self, target):
        """Produces the user interface fragment that should be shown as the
        content for the action's dropdown panel. Returning None indicates the
        action doesn't have a dropdown panel available.

        @param target: The item or content type affected by the action.
        @type target: L{Item<woost.models.item.Item>} instance or class

        @return: The user interface for the action's dropdown panel.
        @rtype: L{Element<cocktail.html.Element>}
        """
        return None

    def get_errors(self, controller, selection):
        """Validates the context of an action before it is invoked.

        @param controller: The controller that invokes the action.
        @type controller: L{Controller<cocktail.controllers.controller.Controller>}

        @param selection: The collection of items that the action will be
            applied to.
        @type selection: L{Item<woost.models.item.Item>} collection

        @return: The list of errors for the indicated context.
        @rtype: iterable L{Exception} sequence
        """
        if not self.ignores_selection:

            # Validate selection size
            selection_size = len(selection) if selection is not None else 0

            if (self.min and selection_size < self.min) \
            or (self.max is not None and selection_size > self.max):
                yield SelectionError(self, selection_size)

    def invoke(self, controller, selection):
        """Delegates control of the current request to the action. Actions can
        override this method to implement their own response logic; by default,
        users are redirected to an action specific controller.

        @param controller: The controller that invokes the action.
        @type controller: L{Controller<cocktail.controllers.controller.Controller>}
        """
        location = Location(self.get_url(controller, selection))
        location.go(client_redirect = self.client_redirect)

    def get_url(self, controller, selection):
        """Produces the URL of the controller that handles the action
        execution. This is used by the default implementation of the L{invoke}
        method. Actions can override this method to alter this value.

        By default, single selection actions produce an URL of the form
        $cms_base_url/content/$selected_item_id/$action_id. Other actions
        follow the form $cms_base_url/$action_id/?selection=$selection_ids

        @param controller: The controller that invokes the action.
        @type controller: L{Controller<cocktail.controllers.controller.Controller>}

        @param selection: The collection of items that the action is invoked
            on.
        @type selection: L{Item<woost.models.item.Item>} collection

        @return: The URL where the user should be redirected.
        @rtype: str
        """
        params = self.get_url_params(controller, selection)

        if self.ignores_selection:
            return controller.contextual_uri(self.id, **params)

        elif self.min == self.max == 1:
            # Single selection
            return controller.edit_uri(
                    selection[0],
                    self.id,
                    **params)
        else:
            return controller.contextual_uri(
                    self.id,
                    selection = [item.id for item in selection],
                    **params)

    def get_url_params(self, controller, selection):
        """Produces extra URL parameters for the L{get_url} method.

        @param controller: The controller that invokes the action.
        @type controller: L{Controller<cocktail.controllers.controller.Controller>}

        @param selection: The collection of items that the action is invoked
            on.
        @type selection: L{Item<woost.models.item.Item>} collection

        @return: A mapping containing additional parameters to include on the
            URL associated to the action.
        @rtype: dict
        """
        params = {}

        if controller.edit_stack:
            params["edit_stack"] = controller.edit_stack.to_param()

        return params

    @getter
    def icon_uri(self):
        return "/resources/images/%s.png" % self.id


class SelectionError(Exception):
    """An exception produced by the L{UserAction.get_errors} method when an
    action is attempted against an invalid number of items."""

    def __init__(self, action, selection_size):
        Exception.__init__(self, "Can't execute action '%s' on %d item(s)."
            % (action.id, selection_size))
        self.action = action
        self.selection_size = selection_size


# Implementation of concrete actions
#------------------------------------------------------------------------------

class CreateAction(UserAction):
    included = frozenset(["toolbar"])
    excluded = frozenset([
        "collection",
        ("selector", "existing_only"),
        "changelog"
    ])
    ignores_selection = True
    min = None
    max = None

    def get_url(self, controller, selection):
        return controller.edit_uri(controller.edited_content_type)


class InstallationSyncAction(UserAction):
    included = frozenset(["toolbar", "item_buttons"])
    content_type = SiteInstallation
    min = 1
    max = 1

    def is_permitted(self, user, target):
        return user.has_permission(InstallationSyncPermission)


class MoveAction(UserAction):
    included = frozenset([("toolbar", "tree")])
    max = None


class AddAction(UserAction):
    included = frozenset([("toolbar", "collection")])
    excluded = frozenset(["integral"])
    ignores_selection = True
    min = None
    max = None

    def invoke(self, controller, selection):

        # Add a relation node to the edit stack, and redirect the user
        # there
        node = RelationNode()
        node.member = controller.relation_member
        node.action = "add"
        controller.edit_stack.push(node)
        controller.edit_stack.go()


class AddIntegralAction(UserAction):

    included = frozenset([("collection", "toolbar", "integral")])
    ignores_selection = True
    min = None
    max = None

    def get_url(self, controller, selection):
        return controller.edit_uri(controller.root_content_type)


class RemoveAction(UserAction):
    included = frozenset([("toolbar", "collection")])
    excluded = frozenset(["integral"])
    max = None

    def invoke(self, controller, selection):

        stack_node = controller.stack_node

        for item in selection:
            stack_node.unrelate(controller.relation_member, item)


class OrderAction(UserAction):
    included = frozenset([("order_content_view", "toolbar")])
    max = None

    def invoke(self, controller, selection):
        node = RelationNode()
        node.member = controller.relation_member
        node.action = "order"
        controller.edit_stack.push(node)
        UserAction.invoke(self, controller, selection)

    def get_url_params(self, controller, selection):
        params = UserAction.get_url_params(self, controller, selection)
        params["member"] = controller.section
        return params


class EditAction(UserAction):
    included = frozenset([
        "toolbar",
        "item_buttons",
        "block_menu",
        "edit_blocks_toolbar"
    ])

    def is_available(self, context, target):

        # Prevent action nesting
        edit_stacks_manager = \
            controller_context.get("edit_stacks_manager")

        if edit_stacks_manager:
            edit_stack = edit_stacks_manager.current_edit_stack
            if edit_stack:
                for node in edit_stack[:-1]:
                    if isinstance(node, EditNode) \
                    and node.item is target:
                        return False

        return UserAction.is_available(self, context, target)

    def is_permitted(self, user, target):
        return user.has_permission(ModifyPermission, target = target)

    def get_url(self, controller, selection):
        return controller.edit_uri(selection[0])


class DeleteAction(UserAction):
    included = frozenset([
        ("content", "toolbar"),
        ("collection", "toolbar", "integral"),
        "item_buttons",
        "block_menu"
    ])
    excluded = frozenset([
        "selector",
        "new_item",
        "calendar_content_view",
        "workflow_graph_content_view",
        "changelog",
        "common_block"
    ])
    max = None

    def is_permitted(self, user, target):
        return user.has_permission(DeletePermission, target = target)


class PreviewAction(UserAction):
    included = frozenset(["item_buttons"])
    content_type = (Publishable, Block)


class OpenResourceAction(UserAction):
    min = 1
    max = 1
    content_type = (Publishable, SiteInstallation, Block)
    included = frozenset([
        "toolbar",
        "item_buttons",
        "edit_blocks_toolbar"
    ])
    excluded = frozenset([
        "new",
        "selector",
        "calendar_content_view",
        "workflow_graph_content_view",
        "changelog"
    ])
    link_target = "_blank"
    client_redirect = True

    def get_url(self, controller, selection):
        target = selection[0]

        if isinstance(target, Publishable):
            return target.get_uri(host = "?")
        elif isinstance(target, Block):
            for path in target.find_paths():
                container = path[0][0]
                if isinstance(container, Publishable):
                    return container.get_uri(host = "?")
            else:
                return "/"
        else:
            return target.url


class ReferencesAction(UserAction):
    included = frozenset([
        "toolbar_extra",
        "item_buttons"
    ])
    min = 1
    max = 1

    def __translate__(self, language, **kwargs):
        label = UserAction.__translate__(self, language, **kwargs)
        if self.stack_node is not None:
            label += " (%d)" % len(self.references)
        return label

    @request_property
    def stack_node(self):
        edit_stacks_manager = \
            controller_context.get("edit_stacks_manager")
        if edit_stacks_manager:
            edit_stack = edit_stacks_manager.current_edit_stack
            if edit_stack:
                return edit_stack[-1]

    @request_property
    def references(self):
        stack_node = self.stack_node

        if not stack_node:
            references = []
        else:
            references = list(self._iter_references(self.stack_node.item))
            references.sort(
                key = lambda ref:
                    (translations(ref[0]), translations(ref[1]))
            )

        return references

    def _iter_references(self, obj):
        for member in obj.__class__.members().itervalues():
            if (
                isinstance(member, schema.RelationMember)
                and member.related_end
                and member.related_end.visible_in_reference_list
                and issubclass(member.related_type, Item)
                and member.related_type.visible
                and not member.integral
            ):
                value = obj.get(member)
                if value:
                    if isinstance(member, schema.Reference):
                        if self._should_include_reference(value, member.related_end):
                            yield value, member.related_end
                    elif isinstance(member, schema.Collection):
                        for item in value:
                            if self._should_include_reference(item, member.related_end):
                                yield item, member.related_end

    def _should_include_reference(self, referrer, relation):
        user = get_current_user()
        return (
            relation.visible
            and user.has_permission(ReadPermission, target = referrer)
            and user.has_permission(ReadMemberPermission, member = relation)
        )


class ShowChangelogAction(UserAction):
    min = None
    max = 1
    excluded = frozenset([
        "selector",
        "new_item",
        "calendar_content_view",
        "changelog",
        "collection"
    ])

    def get_url(self, controller, selection):

        params = self.get_url_params(controller, selection)

        # Filter by target element
        if selection:
            params["filter"] = "member-changes"
            params["filter_value0"] = str(selection[0].id)

        # Filter by target type
        else:
            user_collection = getattr(controller, "user_collection", None)
            if user_collection and user_collection.type is not Item:
                params["filter"] = "target-type"
                params["filter_value0"] = user_collection.type.full_name

        return controller.contextual_uri(
            "changelog",
            **params
        )

    def is_permitted(self, user, target):
        return user.has_permission(ReadHistoryPermission)


class UploadFilesAction(UserAction):
    included = frozenset(["toolbar_extra"])
    content_type = File
    min = None
    max = None
    ignores_selection = True


class ExportAction(UserAction):
    included = frozenset(["toolbar_extra"])
    excluded = UserAction.excluded | frozenset(["collection", "empty_set"])
    min = 1
    max = None
    ignores_selection = True
    format = None
    direct_link = True

    def __init__(self, id, format):
        UserAction.__init__(self, id)
        self.format = format

    def get_url(self, controller, selection):
        return "?" + view_state(
            format = self.format
        )


class InvalidateCacheAction(UserAction):
    min = None
    max = None
    excluded = UserAction.excluded | frozenset(["collection"])

    def invoke(self, controller, selection):

        if selection is None:
            app.cache.clear()
        else:
            for item in selection:
                item.clear_cache()

        notify_user(
            translations("woost.cache_invalidated_notice", subset = selection),
            "success"
        )


class SelectAction(UserAction):
    included = frozenset([("list_buttons", "selector")])
    excluded = frozenset()
    min = None
    max = None

    def invoke(self, controller, selection):

        stack = controller.edit_stack

        if stack:

            node = stack[-1]
            params = {}

            if isinstance(node, SelectionNode):
                params[node.selection_parameter] = (
                    selection[0].id
                    if selection
                    else ""
                )

            elif isinstance(node, RelationNode):
                edit_state = node.parent_node
                member = controller.stack_node.member

                if isinstance(member, schema.Reference):
                    edit_state.relate(
                        member,
                        None if not selection else selection[0]
                    )
                else:
                    if controller.stack_node.action == "add":
                        modify_relation = edit_state.relate
                    else:
                        modify_relation = edit_state.unrelate

                    for item in selection:
                        modify_relation(member, item)

            stack.go_back(**params)


class GoBackAction(UserAction):
    ignores_selection = True
    min = None
    max = None

    def invoke(self, controller, selection):
        controller.go_back()


class CloseAction(GoBackAction):
    included = frozenset([
        "item_buttons",
        "edit_blocks_toolbar"
    ])


class CancelAction(GoBackAction):
    included = frozenset([
        ("list_buttons", "selector")
    ])
    excluded = frozenset()


class SaveAction(UserAction):
    included = frozenset([
        ("item_buttons", "new"),
        ("item_buttons", "edit"),
        ("item_buttons", "preview")
    ])
    ignores_selection = True
    max = None
    min = None
    close = False

    def is_permitted(self, user, target):
        if target.is_inserted:
            return user.has_permission(
                ModifyPermission,
                target = target
            )
        else:
            return user.has_permission(
                CreatePermission,
                target = target.__class__
            )

    def get_errors(self, controller, selection):
        for error in UserAction.get_errors(self, controller, selection):
            yield error

        for error in controller.stack_node.iter_errors():
            yield error

    def invoke(self, controller, selection):
        controller.save_item(close = self.close)


def focus_block(block):
    location = Location.get_current()
    location.hash = "block" + str(block.id)
    location.query_string.pop("action", None)
    location.query_string.pop("block_parent", None)
    location.query_string.pop("block_slot", None)
    location.query_string.pop("block", None)
    location.go("GET")


class EditBlocksAction(UserAction):
    min = 1
    max = 1
    included = frozenset(["toolbar", "item_buttons"])
    excluded = UserAction.excluded | frozenset(["new_item"])

    def is_available(self, context, target):

        if UserAction.is_available(self, context, target):

            if isinstance(target, type):
                content_type = target
            else:
                content_type = type(target)

                # Prevent action nesting
                edit_stacks_manager = \
                    controller_context.get("edit_stacks_manager")

                if edit_stacks_manager:
                    edit_stack = edit_stacks_manager.current_edit_stack
                    if edit_stack:
                        for node in edit_stack:
                            if isinstance(node, EditBlocksNode) \
                            and node.item is target:
                                return False

            return type_is_block_container(content_type)

        return False

    def is_permitted(self, user, target):
        return user.has_permission(ModifyPermission, target = target)

    def get_url(self, controller, selection):

        params = {}
        edit_stack = controller.edit_stack

        if edit_stack:
            params["edit_stack"] = edit_stack.to_param()

        return controller.contextual_uri("blocks", selection[0].id, **params)


class AddBlockAction(UserAction):
    min = None
    max = None
    ignore_selection = True
    included = frozenset(["blocks_slot_toolbar"])
    block_positioning = "append"

    @request_property
    def block_type(self):
        return get_parameter(
            schema.Reference("block_type", class_family = Block)
        )

    @request_property
    def common_block(self):
        return get_parameter(schema.Reference("common_block", type = Block))

    def invoke(self, controller, selection):

        common_block = self.common_block

        # Add a reference to a common block
        if common_block:
            add_block(
                common_block,
                controller.block_parent,
                controller.block_slot,
                positioning = self.block_positioning,
                anchor = controller.block
            )
            datastore.commit()
            focus_block(common_block)

        # Add a new block: set up an edit stack node and redirect the user
        else:
            edit_stacks_manager = controller.context["edit_stacks_manager"]
            edit_stack = edit_stacks_manager.current_edit_stack

            block = self.block_type()
            node = AddBlockNode(
                block,
                visible_translations = controller.visible_languages
            )
            node.block_parent = controller.block_parent
            node.block_slot = controller.block_slot
            node.block_positioning = self.block_positioning
            node.block_anchor = controller.block
            edit_stack.push(node)

            edit_stacks_manager.preserve_edit_stack(edit_stack)
            edit_stack.go()


class AddBlockBeforeAction(AddBlockAction):
    included = frozenset(["block_menu"])
    block_positioning = "before"


class AddBlockAfterAction(AddBlockAction):
    included = frozenset(["block_menu"])
    block_positioning = "after"


class RemoveBlockAction(UserAction):
    content_type = Block
    included = frozenset(["block_menu"])

    def is_available(self, context, target):
        return (
            UserAction.is_available(self, context, target)
            and target.is_common_block()
        )

    def invoke(self, controller, selection):

        collection = controller.block_parent.get(controller.block_slot)

        try:
            index = collection.index(selection[0])
        except ValueError:
            index = None

        schema.remove(collection, selection[0])
        datastore.commit()

        # Focus the block that was nearest to the removed block
        if index is None or not collection:
            adjacent_block = controller.block_parent
        elif index > 0:
            adjacent_block = collection[index - 1]
        else:
            adjacent_block = collection[0]

        focus_block(adjacent_block)


BLOCK_CLIPBOARD_SESSION_KEY = "woost.block_clipboard"

def get_block_clipboard_contents():
    return session.get(BLOCK_CLIPBOARD_SESSION_KEY)

def set_block_clipboard_contents(contents):
    session[BLOCK_CLIPBOARD_SESSION_KEY] = contents


class CopyBlockAction(UserAction):
    content_type = Block
    included = frozenset(["block_menu"])

    def invoke(self, controller, selection):
        set_block_clipboard_contents({
            "mode": "copy",
            "block": controller.block.id,
            "block_parent": controller.block_parent.id,
            "block_slot": controller.block_slot.name
        })
        focus_block(controller.block)


class CutBlockAction(UserAction):
    content_type = Block
    included = frozenset(["block_menu"])

    def invoke(self, controller, selection):
        set_block_clipboard_contents({
            "mode": "cut",
            "block": controller.block.id,
            "block_parent": controller.block_parent.id,
            "block_slot": controller.block_slot.name
        })
        focus_block(controller.block)


class PasteBlockAction(UserAction):
    included = frozenset(["blocks_slot_toolbar"])
    block_positioning = "append"

    def is_available(self, context, target):

        if UserAction.is_available(self, context, target):
            clipboard = get_block_clipboard_contents()
            if clipboard:
                allows_block_type = getattr(target, "allows_block_type", None)
                if (
                    allows_block_type is None
                    or allows_block_type(
                        Block.require_instance(clipboard["block"]).__class__
                    )
                ):
                    return True

        return False

    def invoke(self, controller, selection):
        clipboard = get_block_clipboard_contents()

        if not clipboard:
            notify_user(
                translations("woost.block_clipboard.empty"),
                "error"
            )
        else:
            try:
                block = Block.require_instance(clipboard["block"])
                src_parent = Item.require_instance(clipboard["block_parent"])
                src_slot = type(src_parent).get_member(clipboard["block_slot"])
            except:
                notify_user(
                    translations("woost.block_clipboard.error"),
                    "error"
                )
            else:
                # Remove the block from the source location
                if clipboard["mode"] == "cut":
                    if isinstance(src_slot, schema.Reference):
                        src_parent.set(src_slot, None)
                    elif isinstance(src_slot, schema.Collection):
                        src_collection = src_parent.get(src_slot)
                        schema.remove(src_collection, block)
                # Or copy it
                elif clipboard["mode"] == "copy":
                    block = block.create_copy()
                    block.insert()

                # Add the block to its new position
                add_block(
                    block,
                    controller.block_parent,
                    controller.block_slot,
                    positioning = self.block_positioning,
                    anchor = controller.block
                )

                datastore.commit()
                del session[BLOCK_CLIPBOARD_SESSION_KEY]
                focus_block(block)


class PasteBlockBeforeAction(PasteBlockAction):
    included = frozenset(["block_menu"])
    block_positioning = "before"


class PasteBlockAfterAction(PasteBlockAction):
    included = frozenset(["block_menu"])
    block_positioning = "after"


class ShareBlockAction(UserAction):
    content_type = Block
    included = frozenset(["block_menu"])

    def is_available(self, context, target):
        return UserAction.is_available(self, context, target) \
            and not target.is_common_block()

    def is_permitted(self, user, target):
        config = Configuration.instance
        return (
            UserAction.is_permitted(self, user, target)
            and user.has_permission(ModifyPermission, target = config)
            and user.has_permission(ModifyPermission, target = target)
            and user.has_permission(
                ModifyMemberPermission,
                member = Configuration.common_blocks
            )
        )

    def invoke(self, controller, selection):
        Configuration.instance.common_blocks.append(selection[0])
        datastore.commit()
        focus_block(selection[0])

# Action registration
#------------------------------------------------------------------------------
CreateAction("new").register()
MoveAction("move").register()
AddAction("add").register()
AddIntegralAction("add_integral").register()
RemoveAction("remove").register()
UploadFilesAction("upload_files").register()
AddBlockAction("add_block").register()
AddBlockBeforeAction("add_block_before").register()
AddBlockAfterAction("add_block_after").register()
EditAction("edit").register()
EditBlocksAction("edit_blocks").register()
InstallationSyncAction("installation_sync").register()
CopyBlockAction("copy_block").register()
CutBlockAction("cut_block").register()
PasteBlockAction("paste_block").register()
PasteBlockBeforeAction("paste_block_before").register()
PasteBlockAfterAction("paste_block_after").register()
ShareBlockAction("share_block").register()
RemoveBlockAction("remove_block").register()
DeleteAction("delete").register()
OrderAction("order").register()
ExportAction("export_xls", "msexcel").register()
InvalidateCacheAction("invalidate_cache").register()
ReferencesAction("references").register()
ShowChangelogAction("changelog").register()
OpenResourceAction("open_resource").register()
save_and_close = SaveAction("save_and_close")
save_and_close.close = True
save_and_close.register()
CloseAction("close").register()
CancelAction("cancel").register()
SaveAction("save").register()
PreviewAction("preview").register()
SelectAction("select").register()

