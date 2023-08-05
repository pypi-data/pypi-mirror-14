/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			April 2009
-----------------------------------------------------------------------------*/

cocktail.bind({
    selector: ".BackOfficeLayout",
    behavior: function ($layout) {

        // Disable browser's in-memory caching due to problems going backward
        // and forward between visited pages
        jQuery(window).unload(function() {});

        // Keep alive the current edit_stack
        if (this.edit_stack)
            setTimeout("keepalive('" + this.edit_stack + "')", 300000);
    },
    parts: {
        ".notification:not(.transient)": function ($notification) {

            var closeButton = document.createElement("img");
            closeButton.className = "close_button";
            closeButton.src = "/resources/images/close.png";
            $notification.prepend(closeButton);

            jQuery(closeButton).click(function () {
                $notification.hide("slow");
            });
        }
    }
});

function keepalive(edit_stack) {
    var remoteURL = '/cms/keep_alive?edit_stack=' + edit_stack;
    jQuery.get(remoteURL, function(data) { setTimeout("keepalive('" + edit_stack + "')", 300000); });
}

/* Content drag & drop
-----------------------------------------------------------------------------*/

(function () {

    if (!window.addEventListener) {
        return;
    }

    var UPDATE_DELAY_AFTER_FOREIGN_DROP = 1000;
    var knownDropLocation = false;

    function getPageTop(node) {
        var y = 0;
        while (node) {
            y += node.offsetTop;
            node = node.offsetParent;
        }
        return y;
    }

    // Dragging objects
    cocktail.bind("[data-woost-item]", function ($item) {

        // Dragging objects
        function handleDragStart(e) {
            knownDropLocation = false;
            $item.addClass("drag");
            e.dataTransfer.effectAllowed = "move";
            e.dataTransfer.setData(
                "application/x-woost-item",
                $item.attr("data-woost-item")
            );
            var $icon = $item.find(".icon");
            if ($icon.length) {
                e.dataTransfer.setDragImage($icon.get(0), 10, 10);
            }
            e.stopPropagation();
        }

        function handleDragEnd(e) {
            $item.removeClass("drag");
            if (e.dataTransfer.dropEffect != 'none' && !knownDropLocation) {
                setTimeout(function () { location.reload(); }, UPDATE_DELAY_AFTER_FOREIGN_DROP);
            }
        }

        this.addEventListener("dragstart", handleDragStart, false);
        this.addEventListener("dragend", handleDragEnd, false);
    });

    // Dropping
    cocktail.bind("[data-woost-drop],[data-woost-relativedrop]", function ($receiver) {

        // Dropping on objects
        RELATIVE_INSERT_THRESHOLD = 0.3;
        INSERT_BEFORE = -1;
        APPEND_INSIDE = 0;
        INSERT_AFTER = 1;

        var dropInfo = $receiver.attr("data-woost-drop");
        if (dropInfo) {
            var parts = dropInfo.split(".");
            var dropTargetObject = parts[0];
            var dropTargetMember = parts[1];
        }

        var relativeDropInfo = $receiver.attr("data-woost-relativedrop");
        if (relativeDropInfo) {
            var parts = relativeDropInfo.split(".");
            var relativeDropTargetObject = parts[0];
            var relativeDropTargetMember = parts[1];
            var relativeDropSibling = parts[2];
        }

        function getInsertionMode(element, e) {
            if (relativeDropInfo) {
                var mousePos = 0;
                if (e.pageY) {
                    mousePos = e.pageY;
                }
                else if (e.clientY) {
                    mousePos = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
                }
                var elementTop = getPageTop(element);

                if (dropInfo) {
                    if (mousePos < elementTop + element.offsetHeight * RELATIVE_INSERT_THRESHOLD) {
                        return INSERT_BEFORE;
                    }
                    else if (mousePos > elementTop + element.offsetHeight * (1 - RELATIVE_INSERT_THRESHOLD)) {
                        return INSERT_AFTER;
                    }
                }
                else {
                    if (mousePos < elementTop + element.offsetHeight / 2) {
                        return INSERT_BEFORE;
                    }
                    else {
                        return INSERT_AFTER;
                    }
                }
            }
            return APPEND_INSIDE;
        }

        function clearHighlights() {
            jQuery(".dropReceiver").removeClass("dropReceiver");
            jQuery(".dropBeforeReceiver").removeClass("dropBeforeReceiver");
            jQuery(".dropAfterReceiver").removeClass("dropAfterReceiver");
            jQuery(".dragInsertionMarker").remove();
        }

        function handleDrag(e) {
            var types = e.dataTransfer.types;
            var mimeType = "application/x-woost-item";
            if (types.contains ? types.contains(mimeType) : types.indexOf(mimeType) != -1) {
                clearHighlights();

                if (relativeDropInfo) {
                    var $marker = jQuery("<div class='dragInsertionMarker'>")
                        .appendTo($receiver);
                }

                var mode = getInsertionMode(this, e);

                if (mode == INSERT_BEFORE) {
                    $receiver.addClass("dropBeforeReceiver");
                    $marker
                        .html(cocktail.translate("woost.views.BackOfficeLayout.drop_before"))
                        .css("top", -$marker.height() / 2 + "px");
                }
                else if (mode == INSERT_AFTER) {
                    $receiver.addClass("dropAfterReceiver");
                    $marker
                        .html(cocktail.translate("woost.views.BackOfficeLayout.drop_after"))
                        .css("top", $receiver.height() -$marker.height() / 2 + "px");
                }
                else {
                    $receiver.addClass("dropReceiver");
                    if (relativeDropInfo) {
                        $marker
                            .html(cocktail.translate("woost.views.BackOfficeLayout.drop"))
                            .css("top", $receiver.height() / 2 - $marker.height() / 2 + "px");
                    }
                }

                if (relativeDropInfo) {
                    $marker.css("left", $receiver.width() + 3 + "px")
                }

                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        }

        function handleDrop(e) {
            var data = e.dataTransfer.getData("application/x-woost-item");

            if (data) {
                e.stopPropagation();

                var parameters = { dragged_object: data };
                var mode = getInsertionMode(this, e);

                if (mode == APPEND_INSIDE) {
                    parameters.target_object = dropTargetObject;
                    parameters.target_member = dropTargetMember;
                }
                else {
                    parameters.target_object = relativeDropTargetObject;
                    parameters.target_member = relativeDropTargetMember;
                    parameters.sibling = relativeDropSibling;

                    if (mode == INSERT_BEFORE) {
                        parameters.relative_placement = "before";
                    }
                    else if (mode == INSERT_AFTER) {
                        parameters.relative_placement = "after";
                    }
                }

                jQuery.getJSON("/cms/drop", parameters, function () {
                    location.reload();
                });

                return false;
            }
            knownDropLocation = true;
            clearHighlights();
        }

        this.addEventListener("dragenter", handleDrag, false);
        this.addEventListener("dragover", handleDrag, false);
        this.addEventListener("dragleave", clearHighlights, false);
        this.addEventListener("drop", handleDrop, false);
    });

    cocktail.bind(".ContentList", function ($list) {

        function stopPropagation(e) {
            e.stopPropagation();
            return false;
        }

        this.addEventListener("dragenter", stopPropagation, false);
        this.addEventListener("dragover", stopPropagation, false);
        this.addEventListener("dragleave", stopPropagation, false);
    });

})();

