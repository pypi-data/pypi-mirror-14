/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			November 2013
-----------------------------------------------------------------------------*/

cocktail.bind(".BackOfficeInstallationSyncView", function ($view) {

    var totalItemCount =
          $view.find(".incomming_object").length
        + $view.find(".modified_object").length;

    function toggleSelectionControls() {
        var selectedCount = $checks.filter(":checked").length;

        if (!selectedCount) {
            $selectNone.hide();
        }
        else {
            $selectNone.show();
        }

        if (selectedCount == totalItemCount) {
            $selectAll.hide();
        }
        else {
            $selectAll.show();
        }
    }

    $view.find(".modified_section .modified_object").each(function () {
        var $entry = jQuery(this);

        var $diffDialog = jQuery(cocktail.instantiate("woost.views.BackOfficeInstallationSyncView.diffDialog"));
        $diffDialog.find(".dialog_heading").html($entry.children(".item_label").html());
        $diffDialog.find(".dialog_content").append($entry.children(".object_diff"));

        jQuery(cocktail.instantiate("woost.views.BackOfficeInstallationSyncView.diffDialogButton"))
            .appendTo($entry)
            .click(function () {
                cocktail.showDialog($diffDialog);
                cocktail.center($diffDialog[0]);
            });
    });

    var $checks = $view.find(".item_check")
        .change(toggleSelectionControls);

    var $selectionControls = jQuery(cocktail.instantiate("woost.views.BackOfficeInstallationSyncView.selectionControls"))
        .insertBefore($view.find(".sync_buttons"));

    var $selectAll = $selectionControls.find(".select_all_button")
        .click(function () {
            $checks.attr("checked", "checked");
            toggleSelectionControls();
        });

    var $selectNone = $selectionControls.find(".select_none_button")
        .click(function () {
            $checks.removeAttr("checked");
            toggleSelectionControls();
        });

    toggleSelectionControls();
});

