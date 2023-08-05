#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema

# Add an extension property to control the default member visibility on item listings
schema.Member.listed_by_default = True
schema.Collection.listed_by_default = False
schema.CodeBlock.listed_by_default = False

# Add an extension property to show/hide the 'Element' column on listings
schema.Schema.show_element_in_listings = True

# Add an extension property to show/hide the 'Type' column on listings
schema.Schema.show_type_in_listings = True

# Add an extension property to indicate if members should be visible by users
schema.Member.visible = True

# Add an extension property to indicate if schemas should be instantiable by
# users
schema.Schema.instantiable = True

# Add an extension property to indicate if members should be editable by users
schema.Member.editable = True

# Add an extesnion property to indiciate if members should be shown in detailed view
schema.Member.visible_in_detail_view = True

# Add an extension property to group types
schema.Schema.type_group = None

# Add an extension property to indicate if relations should be excluded if no
# relatable elements exist
schema.Collection.exclude_when_empty = False

# Add an extension property to determine if members should participate in item
# revisions
schema.Member.versioned = True

# Extension property that makes it easier to customize the edit view for a
# collection in the backoffice
schema.Collection.edit_view = None

# Extension property that sets the default type that should be shown by default
# when opening an item selector for the indicated property
schema.RelationMember.selector_default_type = None

# Extension property that allows to indicate that specific members don't modify
# the 'last_update_time' member of items when changed
schema.Member.affects_last_update_time = True

# Extension property that allows hiding relations in the ReferenceList view
schema.RelationMember.visible_in_reference_list = True

# Extension property to select which members should be synchronizable across
# separate site installations
schema.Member.synchronizable = True

