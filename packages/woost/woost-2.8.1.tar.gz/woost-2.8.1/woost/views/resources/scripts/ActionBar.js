/*-----------------------------------------------------------------------------


@author:		Jordi Fernández
@contact:		jordi.fernandez@whads.com
@organization:	Whads/Accent SL
@since:			April 2013
-----------------------------------------------------------------------------*/

cocktail.bind(".ActionBar", function ($actionBar) {

    $actionBar.on("click", "a", function () {
        return !$link.attr("disabled");
    });

    if (!this.selectable) {
        return;
    }

    var $selectable = jQuery(this.selectable);
    if (!$selectable.length) {
        return;
    }

    function toggleButtons() {

        var actionApplicability = {};
        var selection = $selectable[0].getSelection();
        var selectionSize = selection.length;

        for (var i = 0; i < selection.length; i++) {
            var $element = jQuery(selection[i]);
            var elementActions = $element.data("woost-available-actions").split(" ");
            for (var j = 0; j < elementActions.length; j++) {
                var actionId = elementActions[j];
                actionApplicability[actionId] = (actionApplicability[actionId] || 0) + 1;
            }
        }

        $actionBar.find(".action_button").each(function () {
            var $button = jQuery(this);
            if (
                // Check the min/max number of elements allowed by the action
                (
                    !this.ignoresSelection
                    && (
                        (this.minSelection && selectionSize < this.minSelection)
                        || (this.maxSelection && selectionSize > this.maxSelection)
                    )
                )
                // Only enable actions that can be applied to all the elements in the selection
                || (actionApplicability[$button.data("woost-action")] || 0) != selectionSize
            ) {
                $button.attr("disabled", "disabled");
            }
            else {
                $button.removeAttr("disabled");
            }
        });
    }

    $selectable.on("selectionChanged", toggleButtons);
    toggleButtons();
});
