/*-----------------------------------------------------------------------------


@author:		Jordi Fernández
@contact:		jordi.fernandez@whads.com
@organization:	Whads/Accent SL
@since:			March 2014
-----------------------------------------------------------------------------*/

cocktail.bind(".FormAgreementWithPopUp", function ($control) {

    var $dialog = jQuery(cocktail.instantiate("woost.views.FormAgreementWithPopUp.dialog" + "-" + this.id));

    $control.closest(".field").on("click", "a", function () {
        $dialog.find(".dialog_content").load(this.href + " .main > .content", function () {
            cocktail.showDialog($dialog);
            cocktail.center($dialog.get(0));
        });
        return false;
    });
});

