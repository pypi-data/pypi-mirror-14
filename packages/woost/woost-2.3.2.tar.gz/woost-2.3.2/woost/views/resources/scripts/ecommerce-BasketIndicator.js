/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			February 2011
-----------------------------------------------------------------------------*/

cocktail.bind(".BasketIndicator", function ($indicator) {

    function getQueryStringParameterByName(key) {
        key = key.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + key + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    }

    function updateQueryStringParameter(uri, key, value) {
        var re = new RegExp("([?|&])" + key + "=.*?(&|$)", "i");
        separator = uri.indexOf('?') !== -1 ? "&" : "?";
        if (uri.match(re)) {
            return uri.replace(re, '$1' + key + "=" + value + '$2');
        }
        else {
            return uri + separator + key + "=" + value;
        }
    }

    if (woost.ecommerce && woost.ecommerce.order) {
        var $countLabel = jQuery(cocktail.instantiate("woost.extensions.ecommerce.BasketIndicator.count_label"));
        $countLabel.html(woost.ecommerce.order.count_label);
        $indicator.append($countLabel);
    }

    var blinkInterval = null;

    this.blink = function () {

        if (blinkInterval) {
            clearInterval(blinkInterval);
        }

        var blinkStep = 0;
        var LAPSE = 10;
        var STEPS = 60;
        var MIN_OPACITY = 0.25;

        blinkInterval = setInterval(function () {
            blinkStep += 1;
            if (blinkStep >= STEPS) {
                $indicator.css("opacity", "1.0");
                clearInterval(blinkInterval);
            }
            else {
                var x = blinkStep % 20;
                if (x >= 10) x = 10 - (x - 10);
                var o = MIN_OPACITY + (1 - MIN_OPACITY) * x / 10;
                $indicator.css("opacity", o);
            }
        }, LAPSE);
    }

    if (this.blinkOnLoad) {
        this.blink();
    }

    // Preserve catalog url
    var catalogUrl = null;
    var $productListing = jQuery(document).find(".ProductListing");
    if ($productListing.length) {
        catalogUrl = location.href;
    }
    else {
        catalogUrl = getQueryStringParameterByName("catalog_url");
    }

    if (catalogUrl) {
        // Update product urls
        $productListing.find("a").not(
            $productListing.find(".description a")
        ).each(function (i, element) {
            var basketUrl = updateQueryStringParameter(element.href, "catalog_url", encodeURIComponent(catalogUrl));
            element.href = basketUrl;
        });

        // Update basket url
        var basketUrl = updateQueryStringParameter($indicator.attr("href"), "catalog_url", encodeURIComponent(catalogUrl));
        $indicator.attr("href", basketUrl);
    }

});

