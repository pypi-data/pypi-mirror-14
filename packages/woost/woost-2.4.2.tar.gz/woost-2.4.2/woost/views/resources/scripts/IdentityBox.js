/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			December 2013
-----------------------------------------------------------------------------*/

cocktail.bind(".IdentityBox", function ($box) {
    if (woost.user && !woost.user.anonymous) {
        var $boxContent = jQuery(cocktail.instantiate("woost.views.IdentityBox.box"));
        $boxContent.find(".user_label").html(woost.user.label);
        $box.append($boxContent);
    }
});

