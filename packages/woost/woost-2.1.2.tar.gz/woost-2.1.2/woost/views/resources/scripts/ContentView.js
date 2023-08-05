/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			January 2009
-----------------------------------------------------------------------------*/

cocktail.bind(".ContentView", function ($contentView) {

    // Discard the current member / language selection if their dropdown panel
    // is collapsed before submitting the changes
    var $panels = $contentView.find(".collection_settings .DropdownPanel");
    $panels.find(".CheckList .entry input[type=checkbox]").each(function () {
        this.initialCheckState = this.checked;
    });
    $panels.on("collapsed", function () {
        jQuery(this).find(".CheckList .entry input[type=checkbox]").each(function () {
            this.checked = this.initialCheckState;
        });
    });

    var $searchBox = $contentView.find(".simple_search input[type=search]");
    this.searchBox = $searchBox.get(0);

    // Automatically focus the simple search box
    $searchBox.focus();

    // Make the down key pass from the search box to the content
    $searchBox.keydown(function (e) {
        if (e.keyCode == 40) {
            var display = $contentView.find(".collection_display").get(0);
            if (display.focusContent) {
                display.focusContent();
            }
            return false;
        }
    });

    // Make the up key pass from the first entry in the collection to the search box
    var display = $contentView.find(".collection_display").get(0);
    if (display) {
        display.topControl = $searchBox.get(0);
    }

    // Enable/disable buttons depending on the selected content
    function updateToolbar() {
        var display = $contentView.find(".collection_display").get(0);
        if (display && display.getSelection) {
            var selectionSize = display.getSelection().length;
            $contentView.find(".action_button").each(function () {
                if (
                    !this.ignoresSelection
                    && (
                        (this.minSelection && selectionSize < this.minSelection)
                        || (this.maxSelection && selectionSize > this.maxSelection)
                    )
                ) {
                    this.setAttribute("disabled", "disabled");
                }
                else {
                    this.removeAttribute("disabled");
                }
            });
        }
    }

    $contentView.find(".collection_display").bind("selectionChanged", updateToolbar);
    updateToolbar();

    // Replace the 'clear filters' link with a 'discard search' button
    $contentView.find(".filters").each(function () {

        if (jQuery.browser.msie) {
            var closeButton = document.createElement("<input type='button'>");
        }
        else {
            var closeButton = document.createElement("input");
            closeButton.type = "button";
        }

        var $discardButton = jQuery(this).find(".discard_button");
        var closeHref = $discardButton.get(0).href;

        jQuery(closeButton).val(cocktail.translate("woost.views.ContentView close advanced search")).click(function () {
            location.href = closeHref;
        });

        $discardButton.replaceWith(closeButton);
    });

    // Open files in a new window
    $contentView.find(".action_button").click(function() {
        var form = jQuery(this).closest("form").get(0);

        if (jQuery(this).hasClass(".download_action")) {
            form.target = "_new";
        }
        else {
            form.target = "_self";
        }
    });

    // Client side implementation for the addition of filters from table
    // column headers
    if (this.searchExpanded) {
        $contentView.find("th .add_filter")
            .attr("href", "javascript:")
            .click(function () {
                cocktail.foldSelectors();
                var filterBox = $contentView.find(".FilterBox").get(0);
                filterBox.addUserFilter(this.filterId);
            });
    }

    // Reset page value when a new search is done
    $contentView.find(".search_button").click(function () {
        $contentView.find("input[name=page]").val("0");
    });
});

