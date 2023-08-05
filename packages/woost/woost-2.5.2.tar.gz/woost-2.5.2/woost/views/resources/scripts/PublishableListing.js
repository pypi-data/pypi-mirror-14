/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			April 2013
-----------------------------------------------------------------------------*/

cocktail.bind(".PublishableListing .entry .publishable_link", function ($link) {
    $link.click(function () {
        var $view = $link.closest(".entry").find(".publishable_view");
        if ($view.length) {
            var selector = $view.get(0).publishableActivationSelector;
            var $target = $view.is(selector) ? $view : $view.find(selector);
            if ($target.length) {
                $target[0].click();
                return false;
            }
        }
    });
});


