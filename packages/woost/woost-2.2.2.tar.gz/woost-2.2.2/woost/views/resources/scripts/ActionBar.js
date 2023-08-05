/*-----------------------------------------------------------------------------


@author:		Jordi Fernández
@contact:		jordi.fernandez@whads.com
@organization:	Whads/Accent SL
@since:			April 2013
-----------------------------------------------------------------------------*/

cocktail.bind(".ActionBar a", function ($link) {
    $link.click(function () {
        return !$link.attr("disabled");
    });
});
