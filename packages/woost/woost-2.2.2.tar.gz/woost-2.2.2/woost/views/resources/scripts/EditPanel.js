/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			January 2011
-----------------------------------------------------------------------------*/

cocktail.declare("woost");

woost.editURI = function (itemId) {
    return woost.backofficeURI + "/content/" + itemId + "?root_url=" + encodeURIComponent(location.href);
}

cocktail.bind(".EditPanel", function ($panel) {

    this.getExpanded = function () {
        return $panel.hasClass("expanded");
    }

    this.setExpanded = function (expanded) {
        if (expanded) {
            $panel.addClass("expanded");
            jQuery(document.body).addClass("editing");
        }
        else {
            $panel.removeClass("expanded");
            jQuery(document.body).removeClass("editing");
        }
    }

    this.toggleExpanded = function () {
        this.setExpanded(!this.getExpanded());
    }

    // Create a button to show the panel
    jQuery(cocktail.instantiate("woost.views.EditPanel.show_panel_button"))
        .mouseover(function () { $panel.get(0).setExpanded(true); })
        .click(function () { $panel.get(0).setExpanded(true); })
        .appendTo($panel);

    // Create a button to close the panel
    jQuery(cocktail.instantiate("woost.views.EditPanel.close_panel_button"))
        .click(function () { $panel.get(0).setExpanded(false); })
        .appendTo($panel);

    // Block highlighting
    var highlightedBlock = null;

    this.getHighlightedBlock = function () {
        return highlightedBlock;
    }

    this.setHighlightedBlock = function (block) {
        if (block != highlightedBlock) {
            if (highlightedBlock) {
                $panel.find(".block_entry_" + highlightedBlock.blockId).removeClass("highlighted");
                jQuery(highlightedBlock).removeClass("highlighted_block");
            }
            if (block) {
                $panel.find(".block_entry_" + block.blockId).addClass("highlighted");
                jQuery(block).addClass("highlighted_block");
            }
            highlightedBlock = block;
        }
    }

    $panel.find(".block_tree .entry_label")
        .hover(
            function () {
                var $entry = jQuery(this).closest("li");
                $panel.get(0).setHighlightedBlock(
                    jQuery(".block" + $entry.get(0).blockId).get(0)
                );
            },
            function () {
                $panel.get(0).setHighlightedBlock(null);
            }
        );
});

cocktail.bind(".block", function ($block) {
    $block
        .click(function (e) {
            if (jQuery(this).closest("body.editing").length) {
                location.href = woost.editURI(this.blockId);
                return false;
            }
        })
        .mouseenter(function () {
            if (jQuery(this).closest("body.editing").length) {
                jQuery(".EditPanel").get(0).setHighlightedBlock(this);
            }
        })
        .mouseleave(function (e) {
            if (jQuery(this).closest("body.editing").length) {
                var nextBlock = jQuery(e.relatedTarget).closest(".block").get(0);
                jQuery(".EditPanel").get(0).setHighlightedBlock(nextBlock);
            }
        });
});

jQuery(function () {

    // Toggle the visibility of edit panels with a keyboard shortcut
    jQuery(document).keydown(function (e) {
        if (e.keyCode == 69 && e.shiftKey && e.altKey) {
            jQuery(document).find(".EditPanel").each(function () {
                this.toggleExpanded();
            });
            return false;
        }
    });

    // Collapse all edit panels when the document is clicked
    jQuery(document).click(function (e) {
        if (!jQuery(e.target).closest(".EditPanel").length) {
            jQuery(document).find(".EditPanel.expanded").each(function () {
                this.setExpanded(false);
            });
        }
    });
});

