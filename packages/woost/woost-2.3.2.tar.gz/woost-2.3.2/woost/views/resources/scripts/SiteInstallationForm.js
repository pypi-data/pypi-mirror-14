/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			November 2013
-----------------------------------------------------------------------------*/

cocktail.bind(".SiteInstallationForm", function ($form) {

    function togglePasswords() {

        var $passwordField = $form.find(".synchronization_password_field");

        $passwordField.find(".control").val("");

        if (this.checked) {
            $passwordField.show();
        }
        else {
            $passwordField.hide();
        }
    }

    $form.find(".change_password_field .control")
        .each(togglePasswords)
        .click(togglePasswords)
        .change(togglePasswords);
});

