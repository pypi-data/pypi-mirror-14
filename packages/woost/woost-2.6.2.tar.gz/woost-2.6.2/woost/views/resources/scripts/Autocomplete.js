/*-----------------------------------------------------------------------------


@author:        Martí Congost
@contact:       marti.congost@whads.com
@organization:  Whads/Accent SL
@since:         April 2015
-----------------------------------------------------------------------------*/

cocktail.bind(".Autocomplete", function ($autocomplete) {

    var $selectionIcon = jQuery("<img>")
        .addClass("selection_icon")
        .hide()
        .appendTo($autocomplete);

    this.getEntryIcon = function (entry) {

        var icon;

        if (entry) {
            icon = entry.icon;
            if (!icon) {
                var iconFactory = $autocomplete.data("woost-autocomplete-icon-factory");
                if (iconFactory) {
                    icon = "/images/" + entry.value + "/icon16.png";
                }
            }
        }

        return icon;
    }

    function showSelectionIcon() {

        var icon;

        if ($autocomplete.data("woost-autocomplete-show-icons")) {
            icon = $autocomplete[0].getEntryIcon($autocomplete[0].selectedEntry);
            if (!icon) {
                icon = "/resources/images/empty_set.png";
            }
        }

        if (icon) {
            $selectionIcon.attr("src", icon);
            $selectionIcon.show();
        }
        else {
            $selectionIcon.hide();
        }
    }

    $autocomplete.on("change", showSelectionIcon);
    showSelectionIcon();

    this.createEntryDisplay = function (entry) {
        var $display = jQuery("<div>");

        var $label = jQuery("<div>")
            .addClass("label")
            .appendTo($display);

        var iconFactory = $autocomplete.data("woost-autocomplete-icon-factory");
        if (iconFactory) {
            var $icon = jQuery("<img>")
                .addClass("icon")
                .attr("src", this.getEntryIcon(entry))
                .appendTo($label);
        }

        var $textWrapper = jQuery("<span>")
            .addClass("text_wrapper")
            .html(entry.label || entry.text)
            .appendTo($label);

        if (entry.type && $autocomplete.data("woost-autocomplete-show-types")) {
            var $typeLabel = jQuery("<div>")
                .addClass("type_label")
                .html(woost.metadata.types[entry.type].label)
                .appendTo($display);
        }

        return $display;
    }
});

