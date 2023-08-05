#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.html import Element, first_last_classes


class BlockList(Element):

    __wrap = None
    blocks = None
    container = None
    slot = None
    hide_if_empty = False

    def __init__(self, *args, **kwargs):
        Element.__init__(self, *args, **kwargs)
        first_last_classes(self)

    def _build(self):
        self.blocks_container = self

    def _ready(self):
        Element._ready(self)

        if self.blocks is None:
            if self.container is not None and self.slot is not None:
                if isinstance(self.slot, basestring):
                    slot = self.container.__class__.get_member(self.slot)
                else:
                    slot = self.slot

                if slot:
                    self.depends_on(self.container, slot.cache_part)
                    self.blocks = getattr(self.container, slot.name, None)

        if self.tag in ("ul", "ol"):
            self.__wrap = self.wrap_with_list_item
        elif self.tag == "table":
            self.__wrap = self.wrap_with_table_row

        self._fill_blocks()

    def _fill_blocks(self):
        has_visible_blocks = False

        if self.blocks:
            for block in self.blocks:
                self.depends_on(block)
                if block.is_published():
                    has_visible_blocks = True
                    block_view = block.create_view()
                    self._insert_block_view(block_view)

        if self.hide_if_empty and not has_visible_blocks:
            self.visible = False

    def _insert_block_view(self, block_view):
        if self.__wrap:
            entry = self.__wrap(block_view)
            self.blocks_container.append(entry)
        else:
            self.blocks_container.append(block_view)

    def wrap_with_list_item(self, block_view):
        entry = Element("li")
        entry.append(block_view)
        return entry

    def wrap_with_table_row(self, block_view):
        row = Element("tr")
        row.cell = Element("td")
        row.cell.append(block_view)
        row.append(row.cell)
        return row

