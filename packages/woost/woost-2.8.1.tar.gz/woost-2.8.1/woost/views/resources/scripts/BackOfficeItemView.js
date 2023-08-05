/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			April 2009
-----------------------------------------------------------------------------*/

cocktail.bind(".BackOfficeItemView", function ($itemView) {

    // Pending changes control
    var itemView = jQuery(".BackOfficeItemView").get(0);

    if (itemView.closingItemRequiresConfirmation) {

        var hasPendingChanges = itemView.hasPendingChanges;
        var exitPreservesState = undefined;

        $itemView.find(".ContentForm .fields").change(function () {
            hasPendingChanges = true;
        });

        $itemView.on("leavingPage", function (e) {
            exitPreservesState = e.preservingState;
        });

        $itemView.find("form").submit(function () {
            if (exitPreservesState === undefined) {
                exitPreservesState = true;
            }
        });

        $itemView.on("click", ".action_button", function () {
            $itemView.trigger({type: "leavingPage", preservingState: this.value != 'close'});
        });

        window.onbeforeunload = function () {
            if (hasPendingChanges && !exitPreservesState) {
                return cocktail.translate("woost.views.BackOfficeItemView pending changes warning");
            }
        }
    }
});

