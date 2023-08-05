/*-----------------------------------------------------------------------------


@author:        Martí Congost
@contact:       marti.congost@whads.com
@organization:  Whads/Accent SL
@since:         May 2015
-----------------------------------------------------------------------------*/

cocktail.bind(".ThumbnailLink", function ($link) {
    this.setSize = function (width, height) {
        $link.children(".thumbnail").first()
            .outerWidth(width)
            .outerHeight(height);
    }
});

