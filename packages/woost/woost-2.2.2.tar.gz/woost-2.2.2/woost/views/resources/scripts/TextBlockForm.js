/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			July 2012
-----------------------------------------------------------------------------*/

cocktail.bind(".TextBlockForm", function ($form) {

    var $closeUpfields =
        $form.find(".image_close_up_factory_field")
        .add(".image_close_up_preload_field");

    var $check = $form.find(".image_close_up_enabled_field input");

    function toggleCloseUpFields(speed) {
        $closeUpfields[$check.get(0).checked ? "show" : "hide"](speed);
    }

    $check.click(function () { toggleCloseUpFields("slow"); });
    toggleCloseUpFields();
});

