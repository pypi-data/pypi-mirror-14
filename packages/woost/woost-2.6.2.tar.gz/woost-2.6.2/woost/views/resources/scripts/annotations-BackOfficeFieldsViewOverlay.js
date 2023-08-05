/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			February 2014
-----------------------------------------------------------------------------*/

cocktail.bind(".BackOfficeFieldsView .field[data-annotation-target]", function ($field) {

    var $fieldInstances = $field.find(".field_instance");
    var $targetField = $field.closest(".Form").find("." + this.getAttribute("data-annotation-target") + "_field");
    $targetField.addClass("annotationTarget");
    var $targetFieldInstances = $targetField.find(".field_instance");

    $fieldInstances.each(function (index) {

        var $fieldInstance = jQuery(this);
        var $targetFieldInstance = jQuery($targetFieldInstances.get(index));

        var $dropdown = jQuery(cocktail.instantiate("woost.extensions.annotations.FormOverlay.annotationDropdown"))
            .appendTo($targetFieldInstance);

        var $textArea = $fieldInstance.find(".control")
            .appendTo($dropdown.find(".panel"));

        function updateContentHint() {
            if ($textArea.val()) {
                $targetFieldInstance.addClass("with_annotation");
            }
            else {
                $targetFieldInstance.removeClass("with_annotation");
            }
        }

        $textArea.change(updateContentHint);
        updateContentHint();
    });

    $field.remove();
});

