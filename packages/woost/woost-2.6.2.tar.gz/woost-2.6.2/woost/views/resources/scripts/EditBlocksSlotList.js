/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			May 2012
-----------------------------------------------------------------------------*/

// Show the block picker dialog when clicking an 'add' button
cocktail.bind(".EditBlocksSlotList", function ($slotList) {

    var $dialog;

    $slotList.find(".block_picker").click(function () {

        if (!$dialog) {
            $dialog = jQuery(cocktail.instantiate("woost.views.blockPickerDialog"));
            $dialog.addClass("EditBlocksSlotList-block_picker_dialog");
            $dialog.find(".cancel_button").click(function () { cocktail.closeDialog(); });
        }

        $dialog.find("[name=block_parent]").val($slotList.get(0).blockParent);
        $dialog.find("[name=block_slot]").val(jQuery(this).closest(".slot").get(0).blockSlot);
        $dialog.find("[name=action]").val(this.action);

        var blockDisplay = jQuery(this).closest(".BlockDisplay").get(0);
        if (blockDisplay) {
            $dialog.find("[name=block]").val(blockDisplay.block);
        }

        cocktail.showDialog($dialog);
        cocktail.center($dialog.get(0));
        return false;
    });
});

// Fold / unfold slot contents
cocktail.bind(".EditBlocksSlotList.foldable .slot", function ($slot) {

    this.getFolded = function () {
        return $slot.is(".folded");
    }

    this.setFolded = function (folded) {
        if (folded) {
            $slot.addClass("folded");
            addToPersistentFoldList();
        }
        else {
            $slot.removeClass("folded");
            removeFromPersistentFoldList();
        }
    }

    this.toggleFolded = function () {
        this.setFolded(!this.getFolded());
    }

    $slot.children(".slot_header")
        .attr("tabindex", "0")
        .click(function () {
            $slot.get(0).toggleFolded();
            return false;
        });

    var cookieName = "woost.folded_slots";
    var cookieSettings = {path: "/", expires: 60};

    var pkey = $slot.closest(".EditBlocksSlotList").get(0).blockParent + "-" + this.blockSlot;

    function inPersistentFoldList() {
        var list = jQuery.cookie(cookieName);
        if (list) {
            var chunks = list.split(",");
            for (var i = 0; i < chunks.length; i++) {
                if (chunks[i] == pkey) {
                    return true;
                }
            }
        }
        return false;
    }

    function addToPersistentFoldList() {
        if (!inPersistentFoldList()) {
            var list = jQuery.cookie(cookieName);
            if (list) list += ",";
            list += pkey;
            jQuery.cookie(cookieName, list, cookieSettings);
        }
    }

    function removeFromPersistentFoldList() {
        var list = jQuery.cookie(cookieName);
        if (list) {
            var chunks = list.split(",");
            var newList = [];
            for (var i = 0; i < chunks.length; i++) {
                var chunk = chunks[i];
                if (chunk != pkey) {
                    newList.push(chunk);
                }
            }
            jQuery.cookie(cookieName, newList.join(","), cookieSettings);
        }
    }

    if (inPersistentFoldList()) {
        this.setFolded(true);
    }
});

// Drag and drop blocks
(function () {

    var $insertionMarker;
    var insertionParent;
    var insertionAnchor;

    function descendsFrom(node, ancestor) {
        while (node) {
            if (node == ancestor) {
                return true;
            }
            node = node.parentNode;
        }
    }

    function getPageTop(node) {
        var y = 0;
        while (node) {
            y += node.offsetTop;
            node = node.offsetParent;
        }
        return y;
    }

    function getMarker() {
        if (!$insertionMarker) {
            $insertionMarker = jQuery("<div>").addClass("insertion_marker");
        }
        return $insertionMarker;
    }

    function clearMarker() {
        if ($insertionMarker) {
            $insertionMarker.remove();
            $insertionMarker = null;
            insertionParent = null;
            insertionAnchor = null;
        }
    }

    function addToSlot(element, slot, anchor) {
        if (anchor) {
            jQuery(element).insertBefore(anchor);
        }
        else {
            var $blockDisplays = jQuery(slot).children(".BlockDisplay");
            if ($blockDisplays.length) {
                jQuery(element).insertAfter($blockDisplays.last());
            }
            else {
                jQuery(element).prependTo(slot);
            }
        }
    }

    cocktail.bind(".BlockDisplay", function ($blockDisplay) {

        function handleDragStart(e) {
            $blockDisplay.addClass("drag");
            e.dataTransfer.effectAllowed = "move";
            e.dataTransfer.setData(
                "application/x-woost-item",
                JSON.stringify({
                    parent: $blockDisplay.closest(".EditBlocksSlotList").get(0).blockParent,
                    member: $blockDisplay.closest(".slot").get(0).blockSlot,
                    item: this.block
                })
            );
            e.dataTransfer.setDragImage($blockDisplay.find(".block_handle .label").get(0), 10, 10);
            e.stopPropagation();
        }

        function handleDragEnd(e) {
            $blockDisplay.removeClass("drag");
            clearMarker();
        }

        this.addEventListener("dragstart", handleDragStart, false);
        this.addEventListener("dragend", handleDragEnd, false);
    });

    cocktail.bind(".EditBlocksSlotList .slot_blocks", function ($slot) {

        function placeMarker(e) {

            var slot = $slot.get(0);
            var newParent = slot;
            var newAnchor = null;
            var mousePos = 0;

            if (e.pageY) {
                mousePos = e.pageY;
            }
            else if (e.clientY) {
                mousePos = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
            }

            $slot.find(".BlockDisplay").each(function () {
                if (mousePos < getPageTop(this) + this.offsetHeight / 2) {
                    newAnchor = this;
                    newParent = this.parentNode;
                    return false;
                }
            });

            if (insertionParent != newParent || insertionAnchor != newAnchor) {
                insertionParent = newParent;
                insertionAnchor = newAnchor;
                addToSlot(getMarker(), insertionParent, insertionAnchor);
            }
        }

        function handleDrag(e) {
            var types = e.dataTransfer.types;
            var mimeType = "application/x-woost-item";
            if (types.contains ? types.contains(mimeType) : (types.indexOf(mimeType) != -1)) {
                placeMarker(e);
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        }

        function handleDragLeave(e) {
            if (!e.relatedTarget || !descendsFrom(e.relatedTarget, this)) {
                if (insertionParent == this) {
                    clearMarker();
                }
            }
        }

        function handleDrop(e) {
            var data = e.dataTransfer.getData("application/x-woost-item");
            if (data) {
                var dropParent = insertionParent;
                var dropAnchor = insertionAnchor;
                var payload = JSON.parse(data);
                if (payload.parent && payload.member && payload.item) {
                    jQuery.post(
                        "../drop_block",
                        {
                            block: payload.item,
                            source_parent: payload.parent,
                            source_slot: payload.member,
                            target_parent: jQuery(dropParent).closest(".EditBlocksSlotList").get(0).blockParent,
                            target_slot: jQuery(dropParent).closest(".slot").get(0).blockSlot,
                            anchor: (dropAnchor ? dropAnchor.block : "")
                        },
                        function () {
                            var sourceParent = null;
                            jQuery(".EditBlocksSlotList").each(function () {
                                if (this.blockParent == payload.parent) {
                                    sourceParent = this;
                                    return false;
                                }
                            });

                            var sourceSlot = null;
                            jQuery(sourceParent).find(".slot").each(function () {
                                if (this.blockSlot == payload.member) {
                                    sourceSlot = this;
                                    return false;
                                }
                            });

                            var block = null;
                            jQuery(sourceSlot).find(".BlockDisplay").each(function () {
                                if (this.block == payload.item) {
                                    block = this;
                                    return false;
                                }
                            });

                            addToSlot(block, dropParent, dropAnchor);
                        }
                    );
                }
                e.stopPropagation();
            }
        }

        this.addEventListener("dragenter", handleDrag, false);
        this.addEventListener("dragover", handleDrag, false);
        this.addEventListener("dragleave", handleDragLeave, false);
        this.addEventListener("drop", handleDrop, false);
    });
})();

