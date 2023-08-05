/*-----------------------------------------------------------------------------


@author:        Martí Congost
@contact:       marti.congost@whads.com
@organization:  Whads/Accent SL
@since:         May 2015
-----------------------------------------------------------------------------*/

cocktail.bind(".BackOfficeFieldsView", function ($editView) {

    if (typeof(localStorage) != "undefined") {

        var KEY = "woost.extensions.translationworkflow.autoTransitionCheckState";
        var $autoTransitionCheck = $editView.find(".translation_workflow_auto_transition_check");

        function saveAutoTransitionCheckState() {
            localStorage[KEY] = $autoTransitionCheck.is(":checked");
        }

        function restoreAutoTransitionCheckState() {
            if (localStorage[KEY] == "true") {
                $autoTransitionCheck.attr("checked", "checked");
            }
        }

        $autoTransitionCheck.change(saveAutoTransitionCheckState);
        restoreAutoTransitionCheckState();
    }

});

