#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.modeling import OrderedSet, InstrumentedOrderedSet
from cocktail import schema
from cocktail.translations import translations
from cocktail.persistence import transactional
from cocktail.controllers import request_property, get_parameter
from woost.models import (
    Item,
    ModifyPermission,
    ModifyMemberPermission,
    changeset_context,
    get_current_user
)
from woost.controllers.notifications import notify_user
from woost.controllers.backoffice.basebackofficecontroller \
    import BaseBackOfficeController


class DragAndDropController(BaseBackOfficeController):

    rendering_format = "json"

    @request_property
    def dragged_object(self):
        return get_parameter(
            schema.Reference("dragged_object", type = Item)
        )

    @request_property
    def target_object(self):
        return get_parameter(
            schema.Reference("target_object", type = Item)
        )

    @request_property
    def target_member(self):
        eligible_members = [member.name  for member in self.eligible_members]

        if eligible_members:
            member_name = get_parameter(
                schema.String("target_member", enumeration = eligible_members)
            )
            if member_name:
                return self.target_object.__class__.get_member(member_name)

    @request_property
    def eligible_members(self):

        dragged_object = self.dragged_object
        target_object = self.target_object

        if not dragged_object or not target_object:
            return []

        user = get_current_user()

        return [
            member
            for member in target_object.__class__.iter_members()
            if member.visible
            and isinstance(member, schema.RelationMember)
            and member.is_persistent_relation
            and isinstance(dragged_object, member.related_type)
            and user.has_permission(ModifyMemberPermission, member = member)
        ]

    @request_property
    def sibling(self):
        target_member = self.target_member
        if target_member and isinstance(target_member, schema.Collection):
            return get_parameter(
                schema.Reference("sibling",
                    type = target_member.related_type,
                    enumeration = self.target_object.get(target_member)
                )
            )

    @request_property
    def relative_placement(self):
        return get_parameter(
            schema.String("relative_placement", enumeration = ["after", "before"])
        )

    @request_property
    def valid(self):
        return (
            self.dragged_object
            and self.target_object
            and self.target_member
            and (not self.sibling or self.relative_placement)
        )

    def submit(self):

        # TODO: cycle prevention
        # TODO: support for inserting before a sibling
        # TODO: dropping objects on objects (inferring/asking the target member)

        @transactional()
        def relate():
            dragged_object = self.dragged_object
            target_object = self.target_object
            target_member = self.target_member

            user = get_current_user()
            user.require_permission(ModifyPermission, target = dragged_object)
            user.require_permission(ModifyPermission, target = target_object)

            with changeset_context(user):
                if isinstance(target_member, schema.Reference):
                    target_object.set(target_member, dragged_object)
                else:
                    collection = target_object.get(target_member)

                    sibling = self.sibling
                    relative_placement = self.relative_placement

                    if sibling:
                        try:
                            current_index = collection.index(dragged_object)
                        except ValueError:
                            current_index = None
                        index = collection.index(sibling)

                        if relative_placement == "before":
                            if current_index is not None and current_index < index:
                                index -= 1
                        elif relative_placement == "after":
                            if current_index is None or current_index >= index:
                                index += 1

                        if isinstance(
                            collection,
                            (OrderedSet, InstrumentedOrderedSet)
                        ):
                            kwargs = {"relocate": True}
                        else:
                            kwargs = {}

                        collection.insert(index, dragged_object, **kwargs)
                    else:
                        collection.append(dragged_object)
        relate()

        notify_user(
            translations(
                "woost.controllers.backoffice.DragAndDropController"
                ".drop_notification",
                dragged_object = self.dragged_object,
                target_object = self.target_object,
                target_member = self.target_member
            ),
            "success",
            transient = False
        )

    @request_property
    def output(self):
        return {}

