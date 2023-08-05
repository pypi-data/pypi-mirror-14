/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			September 2008
-----------------------------------------------------------------------------*/

cocktail.bind(".BackOfficeEditView", function ($editView) {

    /* Control language visibility
    -----------------------------------------------------------------------------*/
    var languageVisibility = {};

    function persistLanguageVisibility() {
        var visibleLanguages = [];
        for (var lang in languageVisibility) {
            if (languageVisibility[lang]) {
                visibleLanguages.push(lang);
            }
        }
        jQuery.cookie("visible_languages", visibleLanguages.join(','));
    }

    function setLanguageVisibility(language, visible) {
        languageVisibility[language] = visible;
        var method = visible ? "show" : "hide";
        $editView.find(".field_instance." + language)[method]();
    }

    // Restore language visibility from a cookie
    var languageVisibility = {};
    var languages = jQuery.cookie('visible_languages');
    languages = languages ? languages.replace(/"/g,"").replace(/\\054/g, ",").split(',') : cocktail.getLanguages();

    for (var i = 0; i < languages.length; i++) {
        setLanguageVisibility(languages[i], true);
    }

    // Hide all languages not mentioned in the cookie
    $editView.find(".translations_selector li[data-language]").each(function () {
        var language = this.getAttribute("data-language");
        if (!languageVisibility[language]) {
            setLanguageVisibility(language, false);
        }
    });

    // Create the language toggles
    $editView.find(".translations_selector .selector_content li").each( function () {
        if (jQuery(this).find('.language').hasClass('selected')) {

            var language = this.getAttribute("data-language");

            var $check = jQuery("<input>")
                .addClass("translations_check")
                .attr("type", "checkbox")
                .attr("value", language);

            if (languageVisibility[language]) {
                $check.attr("checked", "checked");
            }

            $check
                .click(function () {
                    setLanguageVisibility(this.value, this.checked);
                    persistLanguageVisibility();
                })
                .prependTo(this);
         }
    });

    $editView.find("button[name=add_translation]").click(function () {
        languageVisibility[this.value] = true;
        persistLanguageVisibility();
    });

    /* Turn first level form fieldsets into a tab strip
    -------------------------------------------------------------------------*/
    var $form = $editView.find(".ContentForm").first();

    var $tabStrip = jQuery("<div class='tabStrip'>")
        .prependTo($form);

    var $fieldsets = $form.find(".fields > fieldset");

    $fieldsets.each(function () {
        $tab = jQuery("<button type='button' class='tab'>")
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
            selectTab($tabStrip.children().first().get(0).group);
        }
    }

    jQuery(window).hashchange(trackHash);
    trackHash();
});

