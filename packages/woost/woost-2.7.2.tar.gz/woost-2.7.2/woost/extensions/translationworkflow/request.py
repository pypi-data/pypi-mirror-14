#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.modeling import OrderedSet
from cocktail.translations import translations
from cocktail import schema
from cocktail.schema import expressions as expr
from cocktail.schema.io import MSExcelExporter, MSExcelColumn
from cocktail.html import templates
from woost import app
from woost.models import (
    Item,
    Role,
    User,
    LocaleMember
)
from woost.views.htmldiff import iter_diff_rows
from .state import TranslationWorkflowState
from .translationagency import TranslationAgency
from .utils import (
    get_models_included_in_translation_workflow,
    member_is_included_in_translation_workflow
)


class TranslationWorkflowRequestValues(schema.Mapping):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("searchable", False)
        kwargs.setdefault(
            "display",
            "woost.extensions.translationworkflow.TranslationWorkflowTable"
        )
        schema.Mapping.__init__(self, *args, **kwargs)


class TranslationWorkflowRequest(Item):

    type_group = "translation_workflow"
    instantiable = False
    backoffice_card_view = \
        "woost.extensions.translationworkflow.TranslationWorkflowRequestCard"
    edit_node_class = (
        "woost.extensions.translationworkflow.requesteditnode."
        "TranslationWorkflowRequestEditNode"
    )
    edit_form = (
        "woost.extensions.translationworkflow."
        "TranslationWorkflowRequestForm"
    )

    groups_order = [
        "translation_request.info",
        "translation_request.translated_values",
        "translation_request.changelog",
        "administration"
    ]

    members_order = [
        "translated_item",
        "source_language",
        "target_language",
        "state",
        "assigned_agency",
        "assigned_translator",
        "comments",
        "translated_values"
    ]

    translated_item = schema.Reference(
        type = Item,
        indexed = True,
        bidirectional = True,
        text_search = True,
        editable = schema.NOT_EDITABLE,
        relation_constraints = lambda ctx: [
            expr.IsInstanceExpression(
                expr.Self,
                get_models_included_in_translation_workflow()
            )
        ],
        member_group = "translation_request.info"
    )

    source_language = LocaleMember(
        required = True,
        indexed = True,
        editable = schema.NOT_EDITABLE,
        member_group = "translation_request.info"
    )

    target_language = LocaleMember(
        required = True,
        indexed = True,
        editable = schema.NOT_EDITABLE,
        member_group = "translation_request.info"
    )

    state = schema.Reference(
        type = TranslationWorkflowState,
        required = True,
        related_end = schema.Collection(),
        indexed = True,
        default = schema.DynamicDefault(
            lambda: TranslationWorkflowState.get_instance(
                qname = "woost.extensions.translationworkflow.states.pending"
            )
        ),
        search_control = "cocktail.html.DropdownSelector",
        editable = schema.NOT_EDITABLE,
        searchable = False,
        listed_by_default = False,
        member_group = "translation_request.info"
    )

    assigned_agency = schema.Reference(
        type = TranslationAgency,
        related_end = schema.Collection(),
        indexed = True,
        editable = schema.NOT_EDITABLE,
        member_group = "translation_request.info"
    )

    assigned_translator = schema.Reference(
        type = User,
        related_end = schema.Collection(),
        indexed = True,
        editable = schema.NOT_EDITABLE,
        edit_control = "cocktail.html.Autocomplete",
        search_control = "cocktail.html.Autocomplete",
        member_group = "translation_request.info"
    )

    comments = schema.Collection(
        items = "woost.extensions.translationworkflow.comment."
                "TranslationWorkflowComment",
        bidirectional = True,
        integral = True,
        editable = schema.NOT_EDITABLE,
        member_group = "translation_request.info"
    )

    translated_values = TranslationWorkflowRequestValues(
        member_group = "translation_request.translated_values"
    )

    def apply_translated_values(self):
        language = self.target_language
        for key, value in self.translated_values.iteritems():
            self.translated_item.set(key, value, language)

    def __translate__(self, language, **kwargs):
        if self.source_language and self.target_language:
            return translations(
                "woost.extensions.translationworkflow.request."
                "TranslationWorkflowRequest-instance",
                language,
                instance = self,
                referer = kwargs.get("referer")
            )
        return Item.__translate__(self, language, **kwargs)

    @classmethod
    def backoffice_listing_default_tab(cls):
        for role in app.user.iter_roles():
            default = role.translation_workflow_default_state
            if default is not None:
                return str(default.id)

        return "all"

    @classmethod
    def backoffice_listing_tabs(cls):

        states = OrderedSet()
        for role in app.user.iter_roles():
            states.extend(role.translation_workflow_relevant_states)

        if not states:
            yield (
                "all",
                translations("TranslationWorkflowRequest.tabs.all"),
                None,
                {"state": None}
            )
            states = TranslationWorkflowState.select()

        if states:
            for state in states:
                yield (
                    str(state.id),
                    state.plural_title,
                    cls.state.equal(state),
                    {"state": state}
                )


class MSExcelTranslationWorkflowSourceValuesColumn(MSExcelColumn):

    def get_cell_value(self, obj):
        return [
            obj.translated_item.get(member, language = obj.source_language)
            for member in obj.translated_item.__class__.ordered_members()
            if member_is_included_in_translation_workflow(member)
        ]


class MSExcelTranslationWorkflowTargetValuesColumn(MSExcelColumn):

    def get_cell_value(self, obj):
        return [
            obj.translated_values.get(member.name)
            for member in obj.translated_item.__class__.ordered_members()
            if member_is_included_in_translation_workflow(member)
        ]


class TranslationWorkflowRequestMSExcelExporter(MSExcelExporter):

    def get_member_columns(self, member, languages):
        if member.name == "translated_values":
            yield MSExcelTranslationWorkflowSourceValuesColumn(
                self,
                heading = translations("TranslationWorkflowRequest.msexcel.source")
            )
            yield MSExcelTranslationWorkflowTargetValuesColumn(
                self,
                heading = translations("TranslationWorkflowRequest.msexcel.target")
            )
        else:
            for column in MSExcelExporter.get_member_columns(
                self,
                member,
                languages
            ):
                yield column


TranslationWorkflowRequest.backoffice_msexcel_exporter = \
    TranslationWorkflowRequestMSExcelExporter()


@iter_diff_rows.implementation_for(TranslationWorkflowRequestValues)
def iter_diff_rows(self, language, source, target, source_value, target_value):

    keys = set()
    translated_item = schema.get(source, "translated_item")

    if translated_item is not None:

        translated_model = type(translated_item)

        if source_value is not None:
            keys.update(source_value)

        if target_value is not None:
            keys.update(target_value)

        for key in keys:

            if source_value is None:
                source_subvalue = None
            else:
                source_subvalue = source_value.get(key)

            if target_value is None:
                target_subvalue = None
            else:
                target_subvalue = target_value.get(key)

            if source_value != target_value:
                row = templates.new("woost.views.MemberDiffRow")
                row.diff_member = translated_model.get_member(key)
                row.diff_source = source
                row.diff_target = target
                row.diff_source_value = source_subvalue
                row.diff_target_value = target_subvalue
                yield row

