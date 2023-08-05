/*-----------------------------------------------------------------------------


@author:        Martí Congost
@contact:       marti.congost@whads.com
@organization:  Whads/Accent SL
@since:         April 2015
-----------------------------------------------------------------------------*/

cocktail.bind(".ItemSelector", function ($itemSelector) {

    var member = this.descriptiveMember;
    var $textBox = $itemSelector.find(".text_box");
    var $editButton = $itemSelector.find(".ItemSelector-button.edit");
    var $deleteButton = $itemSelector.find(".ItemSelector-button.delete");
    var $selectionDisplay = $itemSelector.find(".selection_display");

    if (member) {
        $itemSelector.on("click", "[name='relation-new']", function () {
            jQuery("<input type='hidden'>")
                .attr("name", "related_item_" + member)
                .val($textBox.val())
                .appendTo($itemSelector);
        });
    }

    function updateButtons() {

        if ($selectionDisplay.is(".Autocomplete")) {
            var hasValue = $selectionDisplay[0].selectedEntry;
        }
        else if ($selectionDisplay.is("select")) {
            var hasValue = $selectionDisplay.find("option:selected").length;
        }
        else if ($selectionDisplay.is(".RadioSelector")) {
            var hasValue = $selectionDisplay.find("input:checked").length;
        }
        else {
            var hasValue = $selectionDisplay.val()
        }

        if (hasValue) {
            $editButton.show();
            $deleteButton.show();
        }
        else {
            $editButton.hide();
            $deleteButton.hide();
        }
    }

    $itemSelector.change(updateButtons);
    updateButtons();
});

