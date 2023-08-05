/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			March 2014
-----------------------------------------------------------------------------*/

if (window.localStorage && window.JSON) {

    cocktail.bind(".NoticesBox", function ($noticesBox) {

        var STORAGE_KEY = "woost.extensions.notices.hiddenNotices";
        var hiddenNoticesStr = localStorage[STORAGE_KEY];
        var hiddenNotices;

        if (hiddenNoticesStr) {
            try {
                var hiddenNotices = JSON.parse(hiddenNoticesStr);
            }
            catch (ex) {
            }
        }

        if (typeof(hiddenNotices) != 'object') {
            hiddenNotices = {};
        }

        this.hideNotice = function (notice, _persist) {
            jQuery(notice).hide();

            if (!$noticesBox.children(".block:visible").length) {
                $noticesBox.hide();
            }

            if (_persist) {
                hiddenNotices[notice.blockId] = true;
                localStorage[STORAGE_KEY] = JSON.stringify(hiddenNotices);
            }
        }

        for (var blockId in hiddenNotices) {
            jQuery(".block" + blockId).each(function () {
                $noticesBox.get(0).hideNotice(this);
            });
        }

        $noticesBox.children(".block").each(function () {
            var $button = jQuery(cocktail.instantiate("woost.extensions.notices.NoticesBox.closeNoticeButton"))
                .appendTo(this)
                .click(function () {
                    var notice = jQuery(this).closest(".block").get(0);
                    $noticesBox.get(0).hideNotice(notice, true);
                });
        });
    });
}

