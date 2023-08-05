/*-----------------------------------------------------------------------------


@author:        Martí Congost
@contact:       marti.congost@whads.com
@organization:  Whads/Accent SL
@since:         March 2015
-----------------------------------------------------------------------------*/

cocktail.bind(".TranslationWorkflowPathEditor", function ($editor) {

    var $compositeEntry = jQuery(cocktail.instantiate("woost.extensions.translationworkflow.TranslationWorkflowPathEditor.compositeEntry"));
    var $textBox = $editor.find(".text_box");
    $textBox.replaceWith($compositeEntry);
    var $hidden = $compositeEntry.find(".hidden_input");
    var $sourceOptions = $compositeEntry.find(".source_language_selector option");
    var $targetOptions = $compositeEntry.find(".target_language_selector option");

    $editor.on("change", "select", function () {
        var sourceLanguage = $sourceOptions.filter(":selected").val() || "";
        var targetLanguage = $targetOptions.filter(":selected").val() || "";
        $hidden.val(sourceLanguage + ":" + targetLanguage)
    });

    var value = $textBox.val();
    if (value) {
        $hidden.val(value);
        var languages = value.split(":");
        if (languages.length == 2) {
            $sourceOptions.filter("[value='" + languages[0] + "']").attr("selected", "selected");
            $targetOptions.filter("[value='" + languages[1] + "']").attr("selected", "selected");
        }
    }
});

