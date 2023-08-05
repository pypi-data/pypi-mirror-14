#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail.html import templates
from woost.models import Extension, extension_translations

translations.define("TranslationWorkflowExtension",
    ca = u"Circuït de traducció",
    es = u"Circuito de traducción",
    en = u"Translation workflow"
)

translations.define("TranslationWorkflowExtension-plural",
    ca = u"Circuït de traducció",
    es = u"Circuito de traducción",
    en = u"Translation workflow"
)


class TranslationWorkflowExtension(Extension):

    standard_states = (
        {"id": "pending", "color": "#c71e1e"},
        {"id": "ignored", "color": "#666666"},
        {"id": "silenced", "color": "#333333"},
        {"id": "selected", "color": "#e37e20"},
        {"id": "in_translation", "color": "#e6ce18"},
        {"id": "proposed", "color": "#189627"},
        {"id": "applied", "color": "#ffffff"}
    )

    # transition_id: (source_states, target_state)
    standard_transitions = (
        ("ignore", {
            "source_states": [],
            "target_state": "ignored",
            "icon": "ignore"
        }),
        ("silence", {
            "source_states": [],
            "target_state": "silenced",
            "icon": "silence"
        }),
        ("select", {
            "source_states": ["pending", "ignored", "silenced"],
            "target_state": "selected",
            "icon": "forward"
        }),
        ("reject_selection", {
            "source_states": ["selected"],
            "target_state": "pending",
            "icon": "backward"
        }),
        ("assign", {
            "source_states": ["selected", "applied"],
            "target_state": "in_translation",
            "icon": "forward",
            "setup": "woost.extensions.translationworkflow."
                     "assigntransitionsetup."
                     "TranslationWorkflowAssignTransitionSetup",
            "code":
                "from woost.extensions.translationworkflow.translationagency "
                "import TranslationAgency\n"
                "path = request.source_language, request.target_language\n"
                "translator = data['assignments'][path]\n"
                "if isinstance(translator, TranslationAgency):\n"
                "    request.assigned_agency = translator\n"
                "else:\n"
                "    request.assigned_translator = translator"
        }),
        ("propose", {
            "source_states": ["in_translation"],
            "target_state": "proposed",
            "icon": "forward",
            "requires_valid_text": True
        }),
        ("cancel_proposal", {
            "source_states": ["proposed"],
            "target_state": "in_translation",
            "icon": "backward"
        }),
        ("reject", {
            "source_states": ["proposed"],
            "target_state": "in_translation",
            "icon": "backward"
        }),
        ("accept", {
            "source_states": ["proposed"],
            "target_state": "applied",
            "icon": "forward",
            "code": "request.apply_translated_values()"
        })
    )

    def __init__(self, **values):
        Extension.__init__(self, **values)
        self.extension_author = u"Whads/Accent SL"
        self.set("description",
            u"""Gestió avançada de traduccions.""",
            "ca"
        )
        self.set("description",
            u"""Gestión avanzada de traducciones.""",
            "es"
        )
        self.set("description",
            u"""Advanced translation management.""",
            "en"
        )

    def _load(self):
        from woost.extensions.translationworkflow import (
            strings,
            typegroups,
            configuration,
            user,
            item,
            role,
            request,
            comment,
            state,
            transition,
            transitionpermission,
            transitionaction,
        )
        from woost.extensions.translationworkflow.translationagency \
            import TranslationAgency

        # Disable user actions for translation requests
        from woost.controllers.backoffice.useractions import get_user_action
        from .request import TranslationWorkflowRequest

        get_user_action("delete").excluded_content_types.add(
            TranslationWorkflowRequest
        )

        # Register and disable the user actions for each transition
        from cocktail.events import when
        from woost.controllers.backoffice.useractions import get_user_actions
        from woost.controllers.backoffice.basebackofficecontroller \
            import BaseBackOfficeController
        from .transition import TranslationWorkflowTransition
        from .transitionaction \
            import TranslationWorkflowTransitionAction as TWTransAction

        @when(BaseBackOfficeController.before_request)
        def register_transition_user_actions(e):
            for action in get_user_actions():
                if (
                    isinstance(action, TWTransAction)
                    and action.transition is None
                ):
                    action.enabled = False

            for transition in TranslationWorkflowTransition.select(
                order = "relative_order"
            ):
                TWTransAction.register_transition_action(transition)

        # Install the transition controller
        from woost.controllers.backoffice.backofficecontroller \
            import BackOfficeController
        from .transitioncontroller \
            import TranslationWorkflowTransitionController

        BackOfficeController.translation_workflow_transition = \
            TranslationWorkflowTransitionController

        # Install overlays
        from cocktail.html import templates
        for overlay_id in (
            "BackOfficeLayout",
            "BackOfficeFieldsView",
            "ContentView",
            "TranslationDisplay"
        ):
            templates.get_class(
                "woost.extensions.translationworkflow.%sOverlay"
                % overlay_id
            )

        # Optional automatic transition on edit controllers
        from woost.controllers.backoffice.editcontroller import EditController
        from woost.extensions.translationworkflow.defaulttransition \
            import apply_default_transition
        EditController.saving_item.append(apply_default_transition)

        # Count affected translation requests after editing an item
        from cocktail.events import when
        from woost.controllers.backoffice.editstack import EditNode
        from woost.extensions.translationworkflow.utils \
            import notify_translation_request_changes

        @when(EditNode.committed)
        def show_edit_effects_on_translation_workflow(e):
            if e.changeset is not None:
                notify_translation_request_changes(e.changeset)

        # When the manager of a translation agency creates a user, set it up as
        # a translator for the agency automatically
        from woost.models import User, Role
        from woost.controllers.backoffice.editstack import EditNode

        @when(EditNode.saving)
        def link_to_translation_agency(e):

            if e.is_new and isinstance(e.item, User):
                agency = e.user.managed_translation_agency
                if agency is not None:

                    # Register a user as a translator for the agency
                    if e.item not in agency.translators:
                        agency.translators.append(e.item)

                    # Grant the user translator rights
                    translator_role = Role.get_instance(
                        qname = "woost.extensions.translationworkflow."
                                "roles.translators"
                    )
                    if translator_role is not None and not e.item.roles:
                        e.item.roles.append(translator_role)

    def _install(self):
        self.create_standard_graph()
        self.create_standard_access_restrictions()

    def create_standard_graph(self):

        from pkg_resources import resource_filename
        from woost.models import File
        from woost.extensions.translationworkflow import installationstrings
        from woost.extensions.translationworkflow.state \
            import TranslationWorkflowState
        from woost.extensions.translationworkflow.transition \
            import TranslationWorkflowTransition

        # Create all the possible states
        states = {}

        for state_data in self.standard_states:
            state_id = state_data["id"]
            state = self._create_asset(
                TranslationWorkflowState,
                "states." + state_id,
                title = extension_translations,
                plural_title = extension_translations,
                color = state_data["color"]
            )
            states[state_id] = state

        # Setup the state change that should be applied when the source object
        # for a translation request is modified (by default, move the request
        # back to the 'pending' state)
        pending_state = states["pending"]
        silenced_state = states["silenced"]
        for state in states.itervalues():
            if state not in (pending_state, silenced_state):
                state.state_after_source_change = pending_state

        # Create the transitions between states
        rel_order = 0
        icons = {}

        for transition_id, transition_data in self.standard_transitions:

            icon_id = transition_data["icon"]
            icon = icons.get(icon_id)
            if icon is None:
                icons[icon_id] = icon = self._create_asset(
                    lambda:
                        File.from_path(
                            resource_filename(
                                "woost.extensions.translationworkflow",
                                "icons/%s.png" % icon_id
                            ),
                            languages = ()
                        ),
                    "icons." + icon_id,
                    title = extension_translations
                )

            rel_order += 10

            self._create_asset(
                TranslationWorkflowTransition,
                "transitions." + transition_id,
                title = extension_translations,
                source_states = map(
                    states.get,
                    transition_data["source_states"]
                ),
                target_state = states[transition_data["target_state"]],
                relative_order = rel_order,
                transition_setup_class = transition_data.get("setup"),
                transition_code = transition_data.get("code"),
                requires_valid_text = transition_data.get(
                    "requires_valid_text",
                    False
                ),
                icon = icon
            )

    def create_standard_access_restrictions(self):

        from woost.models import (
            Role,
            ReadPermission,
            CreatePermission,
            ModifyPermission,
            DeletePermission,
            ReadMemberPermission
        )
        from woost.extensions.translationworkflow import installationstrings
        from woost.extensions.translationworkflow.request \
            import TranslationWorkflowRequest
        from woost.extensions.translationworkflow.comment \
            import TranslationWorkflowComment
        from woost.extensions.translationworkflow.state \
            import TranslationWorkflowState
        from woost.extensions.translationworkflow.transition \
            import TranslationWorkflowTransition
        from woost.extensions.translationworkflow.transitionpermission \
            import TranslationWorkflowTransitionPermission

        prefix = "woost.extensions.translationworkflow."

        def get_items(cls, *args):
            return [cls.require_instance(qname = prefix + arg) for arg in args]

        # Administrators
        administrators = Role.require_instance(qname = "woost.administrators")
        administrators.permissions.append(
            self._create_asset(
                TranslationWorkflowTransitionPermission,
                "permissions.administrators.transition"
            )
        )

        # Editors
        editors = Role.require_instance(qname = "woost.editors")
        editors.translation_workflow_relevant_states = get_items(
            TranslationWorkflowState,
            "states.pending",
            "states.ignored",
            "states.silenced",
            "states.selected",
            "states.proposed",
            "states.applied"
        )
        editors.translation_workflow_default_state = (
            TranslationWorkflowState.require_instance(
                qname = prefix + "states.pending"
            )
        )
        editors.translation_workflow_default_transition = (
            TranslationWorkflowTransition.require_instance(
                qname = prefix + "transitions.select"
            )
        )
        editors.translation_workflow_default_transition_condition = (
            "applies = (request.state.qname == "
            "'woost.extensions.translationworkflow.states.pending')"
        )
        editors.permissions.append(
            # Allow editors to execute a subset of transitions
            self._create_asset(
                TranslationWorkflowTransitionPermission,
                "permissions.editors.transition",
                transitions = get_items(
                    TranslationWorkflowTransition,
                    "transitions.ignore",
                    "transitions.silence",
                    "transitions.select",
                    "transitions.reject",
                    "transitions.accept"
                )
            )
        )

        # Coordinators
        coordinators = self._create_asset(
            Role,
            "roles.coordinators",
            title = extension_translations,
            default_content_type = TranslationWorkflowRequest,
            translation_workflow_relevant_states = get_items(
                TranslationWorkflowState,
                "states.selected",
                "states.in_translation",
                "states.proposed",
                "states.applied"
            ),
            translation_workflow_default_state = (
                TranslationWorkflowState.require_instance(
                    qname = prefix + "states.selected"
                )
            ),
            permissions = [
                # Allow coordinators to execute a subset of transitions
                self._create_asset(
                    TranslationWorkflowTransitionPermission,
                    "permissions.coordinators.transition",
                    transitions = get_items(
                        TranslationWorkflowTransition,
                        "transitions.reject_selection",
                        "transitions.assign"
                    )
                ),
                # See all requests
                self._create_asset(
                    ReadPermission,
                    "permissions.coordinators.read_requests",
                    content_type = TranslationWorkflowRequest
                ),
                # Read comments
                self._create_asset(
                    ReadPermission,
                    "permissions.coordinators.read_comments",
                    content_type = TranslationWorkflowComment
                ),
                # Make comments
                self._create_asset(
                    CreatePermission,
                    "permissions.coordinators.write_comments",
                    content_type = TranslationWorkflowComment
                ),
                # Limit the members they can see
                self._create_asset(
                    ReadMemberPermission,
                    "permissions.coordinators.read_members",
                    matching_members =
                        [
                            "woost.models.item.Item." + k
                            for k in [
                                "id",
                                "creation_time",
                                "last_update_time",
                                "author"
                            ]
                        ]
                        + [
                            prefix + "request.TranslationWorkflowRequest." + k
                            for k in [
                                "translated_item",
                                "source_language",
                                "target_language",
                                "state",
                                "assigned_translator",
                                "comments",
                                "translated_values"
                            ]
                        ]
                ),
                # Deny everything else
                self._create_asset(
                    CreatePermission,
                    "permissions.coordinators.deny_create",
                    authorized = False
                ),
                self._create_asset(
                    ModifyPermission,
                    "permissions.coordinators.deny_modify",
                    authorized = False
                ),
                self._create_asset(
                    DeletePermission,
                    "permissions.coordinators.deny_delete",
                    authorized = False
                ),
                self._create_asset(
                    ReadMemberPermission,
                    "permissions.coordinators.deny_read_members",
                    authorized = False
                )
            ]
        )

        # Translators
        translators = self._create_asset(
            Role,
            "roles.translators",
            title = extension_translations,
            default_content_type = TranslationWorkflowRequest,
            translation_workflow_relevant_states = get_items(
                TranslationWorkflowState,
                "states.in_translation",
                "states.proposed",
                "states.applied"
            ),
            translation_workflow_default_state = (
                TranslationWorkflowState.require_instance(
                    qname = prefix + "states.in_translation"
                )
            ),
            permissions = [
                # Allow translators to execute a subset of transitions
                self._create_asset(
                    TranslationWorkflowTransitionPermission,
                    "permissions.translators.transition",
                    transitions = get_items(
                        TranslationWorkflowTransition,
                        "transitions.propose",
                        "transitions.cancel_proposal"
                    )
                ),
                # Allow translators to see their assigned requests
                self._create_asset(
                    ReadPermission,
                    "permissions.translators.read_requests",
                    subject_description = extension_translations,
                    content_type = TranslationWorkflowRequest,
                    content_expression =
                        "items.add_filter(cls.assigned_translator.equal(user))"
                ),
                # Allow translators to modify their assigned translation
                # requests
                self._create_asset(
                    ModifyPermission,
                    "permissions.translators.modify_assigned_requests",
                    subject_description = extension_translations,
                    content_type = TranslationWorkflowRequest,
                    content_expression =
                        "from woost.extensions.translationworkflow.state \\\n"
                        "    import TranslationWorkflowState\n"
                        "in_translation = TranslationWorkflowState.require_instance(\n"
                        "    qname = 'woost.extensions.translationworkflow.states.in_translation'\n"
                        ")\n"
                        "items.add_filter(cls.state.equal(in_translation))\n"
                        "items.add_filter(cls.assigned_translator.equal(user))"
                ),
                # Allow translators to see comments for their assigned requests
                self._create_asset(
                    ReadPermission,
                    "permissions.translators.read_comments",
                    subject_description = extension_translations,
                    content_type = TranslationWorkflowComment,
                    content_expression =
                        "from woost.extensions.translationworkflow.request \\\n"
                        "    import TranslationWorkflowRequest as TWRequest\n"
                        "assigned_requests = TWRequest.select(\n"
                        "    TWRequest.assigned_translator.equal(user)\n"
                        ")\n"
                        "items.add_filter(cls.request.one_of(assigned_requests))"
                ),
                # Comment requests assigned to them
                self._create_asset(
                    CreatePermission,
                    "permissions.translators.write_comments",
                    subject_description = extension_translations,
                    content_type = TranslationWorkflowComment,
                    content_expression =
                        "from woost.extensions.translationworkflow.request \\\n"
                        "    import TranslationWorkflowRequest as TWRequest\n"
                        "assigned_requests = TWRequest.select(\n"
                        "    TWRequest.assigned_translator.equal(user)\n"
                        ")\n"
                        "items.add_filter(cls.request.one_of(assigned_requests))"
                ),
                # Limit the members they can see
                self._create_asset(
                    ReadMemberPermission,
                    "permissions.translators.read_members",
                    matching_members =
                        [
                            "woost.models.item.Item." + k
                            for k in [
                                "id",
                                "creation_time",
                                "last_update_time",
                                "author"
                            ]
                        ]
                        + [
                            prefix + "request.TranslationWorkflowRequest." + k
                            for k in [
                                "translated_item",
                                "source_language",
                                "target_language",
                                "state",
                                "comments",
                                "translated_values"
                            ]
                        ]
                ),
                # Deny everything else
                self._create_asset(
                    CreatePermission,
                    "permissions.translators.deny_create",
                    authorized = False
                ),
                self._create_asset(
                    ModifyPermission,
                    "permissions.translators.deny_modify",
                    authorized = False
                ),
                self._create_asset(
                    DeletePermission,
                    "permissions.translators.deny_delete",
                    authorized = False
                ),
                self._create_asset(
                    ReadMemberPermission,
                    "permissions.translators.deny_read_members",
                    authorized = False
                )
            ]
        )

