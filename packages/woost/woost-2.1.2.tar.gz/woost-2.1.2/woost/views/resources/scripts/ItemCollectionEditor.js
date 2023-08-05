/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			July 2012
-----------------------------------------------------------------------------*/

cocktail.bind(".ItemCollectionEditor", function ($editor) {

    // Enable/disable buttons depending on the selected content
    function updateToolbar() {
        var selection = $editor.get(0).getSelection();
        var selectionSize = selection.length;
        $editor.find(".action_button").each(function () {
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

    $editor.bind("selectionChanged", updateToolbar);
    updateToolbar();

    // Double click to edit
    $editor.bind("activated", function () {
        $editor.find(".edit_action").click();
    });

    // Enable drag & drop sorting
    $editor.find("ul.entries").sortable({axis: "y"});
});

