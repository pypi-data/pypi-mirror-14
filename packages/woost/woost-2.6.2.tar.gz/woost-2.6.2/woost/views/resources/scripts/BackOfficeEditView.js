/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			September 2008
-----------------------------------------------------------------------------*/

cocktail.bind(".BackOfficeEditView", function ($editView) {

    /* Turn first level form fieldsets into a tab strip
    -------------------------------------------------------------------------*/
    var $form = $editView.find(".ContentForm").first();

    var $fieldsets = $form.find(".fields > fieldset");
    if ($fieldsets.length < 2) {
        return;
    }

    var $tabStrip = jQuery("<div class='tab_strip'>")
        .prependTo($form);

    $fieldsets.each(function () {
        $tab = jQuery("<button type='button' class='tab_strip_entry'>")
            .addClass(this.group)
            .html(jQuery(this).children("legend").html())
            .appendTo($tabStrip)
            .click(function () { location.hash = this.group; });
        $tab.get(0).group = this.group;
    });

    function selectTab(group) {

        var $tab = $tabStrip.children("." + group);
        var $fieldset = $fieldsets.filter("." + group);

        if ($tab.length && $fieldset.length) {
            $tabStrip.children().removeClass("selected");
            $fieldsets.removeClass("selected");
            $tab.addClass("selected");
            $fieldset.addClass("selected");
            location.hash = group;
            $editView.find("input[type=hidden][name=tab]").val(group);
        }
    }

    function trackHash() {
        var tabSelected = false;

        if (location.hash) {
            var group = location.hash.substr(1);
            if ($tabStrip.children("." + group).length) {
                tabSelected = true;
                selectTab(group);
            }
        }

        if (!tabSelected) {
            var tab = $tabStrip.children().first().get(0);
            if (tab) {
                selectTab(tab.group);
            }
        }
    }

    jQuery(window).hashchange(trackHash);
    trackHash();

    /* Focus the first available field
    -------------------------------------------------------------------------*/
    $editView.find(".field :input:visible[tabindex!='-1']").each(function () {
        if (!jQuery(this).parents("[data-cocktail-editable='read_only']").length) {
            this.focus();
            return false;
        }
    });
});

