/*-----------------------------------------------------------------------------


@author:        Martí Congost
@contact:       marti.congost@whads.com
@organization:  Whads/Accent SL
@since:         February 2015
-----------------------------------------------------------------------------*/

(function () {
    var PREFIX = "data-woost-context-menu";
    var MIN_CONNECTOR_POSITION = 14;

    var ALIGNMENTS = [
        ["bottom", "right"],
        ["bottom", "left"],
        ["top", "right"],
        ["top", "left"]
    ];

    cocktail.bind(".ItemContextMenu", function ($menu) {

        var $owner = this.menuOwnerSelector ? $menu.closest(this.menuOwnerSelector) : $menu.parent();

        if (this.menuOriginSelector) {
            var $origin =
                $owner.find(this.menuOriginSelector)
                .not($menu.find(this.menuOriginSelector))
                .first();
            if (!$origin.length) {
                $origin = $owner;
            }
        }
        else {
            $origin = $owner;
        }
        $menu.insertAfter($origin);

        var itemId = $menu.attr("data-woost-item");
        var $panel = $menu.find(".panel");
        var $connector = null;
        var currentConnectorPosition = undefined;

        this.getExpanded = function () {
            return $menu.attr(PREFIX + "-state") == "expanded";
        }

        this.setExpanded = function (expanded, connectorPosition /* undefined */) {
            if (expanded) {
                closeExpandedDisplay();
                if (connectorPosition !== undefined) {
                    connectorPosition = Math.max(connectorPosition, MIN_CONNECTOR_POSITION);
                }
                currentConnectorPosition = connectorPosition;

                if (!$connector) {
                    $connector = jQuery("<canvas>")
                        .addClass("panel_connector")
                        .appendTo($menu);
                }
            }
            $owner.attr(PREFIX, expanded ? "expanded" : "closed");
            $menu.attr(PREFIX + "-state", expanded ? "expanded" : "closed");
            // Position the panel
            if (expanded) {
                this.alignPanel();
            }
        }

        this.alignPanel = function () {
            for (var i = 0; i < ALIGNMENTS.length; i++) {
                var valign = ALIGNMENTS[i][0];
                var halign = ALIGNMENTS[i][1];
                $menu.attr(PREFIX + "-valign", valign);
                $menu.attr(PREFIX + "-halign", halign);

                $connector.css("left",
                    (currentConnectorPosition === undefined ?
                        $origin.outerWidth() / 2
                        : Math.min(
                            $panel.outerWidth() - MIN_CONNECTOR_POSITION,
                            halign == "right" ?
                                currentConnectorPosition
                                : $panel.outerWidth() - $origin[0].offsetWidth + currentConnectorPosition
                        )
                    )
                    - $connector.outerWidth() / 2
                    + "px"
                );

                if (halign == "right") {
                    $menu.css("left", $origin[0].offsetLeft);
                }
                else if (halign == "left") {
                    $menu.css("left", $origin[0].offsetLeft + $origin[0].offsetWidth - $panel.outerWidth() + "px");
                }

                if (valign == "bottom") {
                    $menu.css("top", $origin[0].offsetTop + $origin.outerHeight() + "px");
                    $connector.css("top", "0");
                    $panel.css("top", $connector.outerHeight() - 1 + "px");
                }
                else if (valign == "top") {
                    $menu.css("top", $origin[0].offsetTop - $connector.outerHeight() - $panel.outerHeight() + "px");
                    $connector.css("top", $panel.outerHeight() + "px");
                    $panel.css("top", "1px");
                }

                // Make sure the panel fits the viewport; otherwise, try the next alignment
                var pos = getPosition($panel[0]);
                if (
                    pos.left >= document.body.scrollLeft
                    && pos.right < document.body.scrollLeft + jQuery(window).width()
                    && pos.top >= document.body.scrollTop
                    && pos.bottom < document.body.scrollTop + jQuery(window).height()
                ) {
                    break;
                }
            }
            this.drawPanelConnector();
        }

        this.drawPanelConnector = function () {

            var valign = jQuery(this).attr(PREFIX + "-valign");

            var w = $connector.width();
            var h = $connector.height();
            $connector[0].width = w;
            $connector[0].height = h;

            var ctx = $connector[0].getContext("2d");
            ctx.save();
            ctx.fillStyle = $panel.css("background-color");
            ctx.strokeStyle = $panel.css("border-left-color");

            if (valign == "top") {
                ctx.moveTo(0, 0);
                ctx.lineTo(w / 2, h);
                ctx.lineTo(w, 0);
            }
            else if (valign == "bottom") {
                ctx.moveTo(0, h);
                ctx.lineTo(w / 2, 0);
                ctx.lineTo(w, h);
            }

            ctx.fill();
            ctx.stroke();
            ctx.restore();
        }

        this.toggleExpanded = function (connectorPosition /* optional */) {
            this.setExpanded(!this.getExpanded(), connectorPosition);
        }

        $owner.on("contextmenu", function (e) {
            var clickPosition = e.pageX - $origin.offset().left;
            $menu.get(0).toggleExpanded(clickPosition);

            var effectOnSelection = $menu[0].effectOnSelection;
            if (effectOnSelection) {
                $owner.parents().each(function () {
                    if (this.selectEntries) {
                        if (effectOnSelection == "change" || effectOnSelection == "clear") {
                            this.clearSelection();
                        }
                        if (effectOnSelection == "change") {
                            this.selectEntries($owner.closest(this.entrySelector));
                        }
                    }
                });
            }

            return false;
        });

        // Consume all "click" events on the panel; only allow
        // clicks on buttons to pass through.
        $panel.click(function (e) {
            var node = e.target;
            while (node != $panel[0]) {
                if (node.tagName == "BUTTON" || (node.tagName == "INPUT" && node.type == "submit")) {
                    return true;
                }
                node = node.parentNode;
            }
            e.stopPropagation();
        });

        this.setExpanded(false);
    });

    function getPosition(element) {
        var pos = {left: 0, top: 0, right: element.offsetWidth, bottom: element.offsetHeight};
        while (element) {
            pos.left += element.offsetLeft;
            pos.top += element.offsetTop;
            element = element.offsetParent;
        }
        pos.right += pos.left;
        pos.bottom += pos.top;
        return pos;
    }

    function closeExpandedDisplay() {
        jQuery(".ItemContextMenu[" + PREFIX + "-state='expanded']").each(function () {
            this.setExpanded(false);
        });
    }

    jQuery(function () {
        jQuery(document).click(closeExpandedDisplay);
        jQuery(document).on("contextmenu", closeExpandedDisplay);
        jQuery(window).resize(function () {
            jQuery(".ItemContextMenu[" + PREFIX + "-state='expanded']").each(function () {
                this.alignPanel();
            });
        });
    });
})();

