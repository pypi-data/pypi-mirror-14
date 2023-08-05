/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			February 2014
-----------------------------------------------------------------------------*/

cocktail.bind(".ItemTranslationsSelector", function ($selector) {

    var $searchControls = jQuery(cocktail.instantiate("woost.views.ItemTranslationsSelector.searchControls"))
        .prependTo(this);

    var $searchBox = $searchControls.find(".search_box")
        .keydown(function (e) {
            if (e.keyCode == 40) {
                $selector.find(".defined_languages_section .language_list").get(0).focusContent();
                return false;
            }
        });

    var $languageLists = $selector.find(".language_list");

    $languageLists.each(function (index) {

        var checkList = this;
        var $checkList = jQuery(this);
        checkList.topControl = $searchBox.get(0);

        var $selectionControls = jQuery(cocktail.instantiate("woost.views.ItemTranslationsSelector.selectionControls"))
            .insertAfter(this);

        var $selectAllLink = $selectionControls.find(".select_all_link")
            .click(function () {
                checkList.selectEntries(":selectable-entry");
            });

        var $selectNoneLink = $selectionControls.find(".select_none_link")
            .click(function () {
                checkList.clearSelection(":selectable-entry");
            });

        function toggleSelectionLinks() {
            var $allEntries = checkList.getEntries(":selectable-entry");
            var $selectedEntries = $allEntries.filter(".selected");

            if ($allEntries.length > $selectedEntries.length) {
                $selectAllLink.removeAttr("disabled");
            }
            else {
                $selectAllLink.attr("disabled", "disabled");
            }

            if ($selectedEntries.length) {
                $selectNoneLink.removeAttr("disabled");
            }
            else {
                $selectNoneLink.attr("disabled", "disabled");
            }
        }

        $selector.on("searched", toggleSelectionLinks);
        $selector.on("containingDropdownExpanded", toggleSelectionLinks);
        $checkList.on("selectionChanged", toggleSelectionLinks);

        $checkList.on("keydown", ".entry", function (e) {
            var sibling = null;
            if (e.keyCode == 37) {
                if (index > 0) {
                    sibling = $languageLists.get(index - 1);
                }
            }
            else if (e.keyCode == 39) {
                if (index + 1 < $languageLists.length) {
                    sibling = $languageLists.get(index + 1);
                }
            }
            if (sibling) {
                sibling.focusContent();
                return false;
            }
        });
    });

    cocktail.searchable(this);
    this.applySearch($searchControls.find(".search_box").val());
});

