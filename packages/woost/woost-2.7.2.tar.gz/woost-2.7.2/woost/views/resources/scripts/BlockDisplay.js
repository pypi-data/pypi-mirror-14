/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			November 2012
-----------------------------------------------------------------------------*/

cocktail.bind(".BlockDisplay", function ($block) {

    function activate(action) {
        var $button = $block.children(".block_handle").find("[data-woost-action='" + action + "']");
        $button.click();
        return $button.length;
    }

    $block.dblclick(function () {
        activate("edit");
        return false;
    });

    $block.keydown(function (e) {

        // Up: focus previous block
        if (e.keyCode == 38) {
            var $list = $block.parents(".EditBlocksSlotList").last();
            var $blocks = $list.find(".BlockDisplay");
            if (e.altKey && $block.parents(".BlockDisplay").length) {
                $blocks = $blocks.not(
                    $block.prevAll(".BlockDisplay")
                    .find(".BlockDisplay")
                    .andSelf()
                );
            }
            var index = $blocks.index(this);
            if (index > 0) {
                $blocks[index - 1].focus();
            }
            return false;
        }
        // Down: focus next block
        else if (e.keyCode == 40) {
            var $list = $block.parents(".EditBlocksSlotList").last();
            var $blocks = $list.find(".BlockDisplay");
            if (e.altKey) {
                $blocks = $blocks.not($block.find(".BlockDisplay"));
            }
            var index = $blocks.index(this);
            if (index + 1 < $blocks.length) {
                $blocks[index + 1].focus();
            }
            return false;
        }
        // Home: focus the first block
        else if (e.keyCode == 36) {
            var $list = $block.parents(".EditBlocksSlotList").last();
            $list.find(".BlockDisplay").first().focus();
            return false;
        }
        // End: focus the last block
        else if (e.keyCode == 35) {
            var $list = $block.parents(".EditBlocksSlotList").last();
            $list.find(".BlockDisplay").last().focus();
            return false;
        }
        // b: add before
        else if (e.keyCode == 66) {
            $block.find(".block_handle .block_picker.add_block_before").click();
            return false;
        }
        // a: add after
        else if (e.keyCode == 65) {
            $block.find(".block_handle .block_picker.add_block_after").click();
            return false;
        }
        // Enter: edit the block
        else if (e.keyCode == 13) {
            activate("edit");
            return false;
        }
        // Delete: remove the block
        else if (e.keyCode == 46) {
            activate("delete") || activate("remove_block");
            return false;
        }
        // Ctrl + c: copy
        else if (e.keyCode == 67 && e.ctrlKey) {
            activate("copy_block");
            return false;
        }
        // Ctrl + x: cut
        else if (e.keyCode == 88 && e.ctrlKey) {
            activate("cut_block");
            return false;
        }
        // Ctrl + v: paste
        else if (e.keyCode == 86 && e.ctrlKey) {
            activate("paste_block_after");
            return false;
        }
    });
});

jQuery(function () {
    if (location.hash) {
        jQuery(location.hash).focus();
    }
    else {
        jQuery(".BlockDisplay").first().focus();
    }
});

