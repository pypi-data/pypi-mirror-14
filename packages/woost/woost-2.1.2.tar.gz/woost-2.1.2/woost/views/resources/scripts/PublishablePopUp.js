/*-----------------------------------------------------------------------------


@author:		Jordi Fernández
@contact:		jordi.fernandez@whads.com
@organization:	Whads/Accent SL
@since:			March 2013
-----------------------------------------------------------------------------*/

cocktail.bind(".PublishablePopUp", function ($popUp) {

    this.createDialog = function () {
        if (!this.dialog) {
            this.dialog = cocktail.instantiate("woost.views.PublishablePopUp.dialog_" + this.id);
        }
        return this.dialog;
    };

    this.showDialog = function () {
        var dialog = this.createDialog();
        cocktail.showDialog(dialog);
        cocktail.init(dialog);
        cocktail.center(dialog);
    };

    $popUp.click(function (e) {
        $popUp.get(0).showDialog();
        return false;
    });
});

