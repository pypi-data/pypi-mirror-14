/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			January 2011
-----------------------------------------------------------------------------*/

cocktail.bind({
    selector: ".ImageGallery",
    behavior: function ($imageGallery) {

        var loadedImages = {};
        var singleImage = ($imageGallery.find(".image_entry").length < 2);

        $imageGallery.bind("imageLoaded", function (e, loadedImage) {
            loadedImages[loadedImage.src] = loadedImage;
        });

        this.loadImage = function (src, callback /* optional */, showStatus /* optional */) {

            var image = loadedImages[src];

            if (image && image.loaded) {
                if (callback) {
                    callback.call(this, image);
                }
            }
            else {
                if (showStatus) {
                    this.setLoading(true);
                }

                if (callback) {
                    var handler = function (e, loadedImage) {
                        if (loadedImage.src == src) {
                            $imageGallery.unbind("imageLoaded", handler);
                            callback.call(this, loadedImage);
                        }
                    }
                    $imageGallery.bind("imageLoaded", handler);
                }

                if (!image) {
                    image = new Image();
                    loadedImages[src] = image;
                    image.onload = function () {
                        this.loaded = true;
                        if (image.showStatus) {
                            $imageGallery.get(0).setLoading(false);
                        }
                        $imageGallery.trigger("imageLoaded", this);
                    }
                    image.showStatus = showStatus;
                    image.src = src;
                }
                else if (showStatus) {
                    image.showStatus = true;
                }
            }
        }

        this.setLoading = function (loading) {
            var $sign = jQuery(".ImageGallery-loading_sign");

            if (!loading) {
                clearInterval($sign.get(0).animationTimer);
                $sign.remove();
            }
            else if (!$sign.length) {
                var sign = cocktail.instantiate("woost.views.ImageGallery.loading_sign");
                sign.animationStep = 0;
                sign.ball = document.createElement("div");
                sign.ball.className = "ball";
                sign.appendChild(sign.ball);
                sign.animationTimer = setInterval(function () {
                    sign.animationStep = (sign.animationStep + 1) % 200;
                    if (sign.animationStep < 100) {
                        var pos = sign.animationStep;
                    }
                    else {
                        var pos = 200 - sign.animationStep;
                    }
                    sign.ball.style.left = sign.offsetWidth / 4 + (sign.offsetWidth / 2 * pos / 100) + "px";
                }, 10);
                document.body.appendChild(sign);
                cocktail.center(sign);
            }
        }

        var $dialog = null;

        this.showImage = function (entry) {

            cocktail.closeDialog();
            $dialog = jQuery(this.createImageDialog(entry));
            cocktail.showDialog($dialog.get(0));
            $dialog.hide();

            // Show the dialog once the image finishes loading
            this.loadImage(
                jQuery(entry).find(".image_link").get(0).href,
                function (image) {
                    $dialog.find(".dialog_content .image")
                        .width(image.width)
                        .height(image.height);

                    $dialog.find(".footnote")
                        .width(image.width);

                    var $next = $dialog.find(".next_button");
                    $next.css("top", image.height / 2 - $next.get(0).offsetHeight / 2 + "px");

                    var $prev = $dialog.find(".previous_button");
                    $prev.css("top", image.height / 2 - $prev.get(0).offsetHeight / 2 + "px");

                    $dialog.show();
                    cocktail.center($dialog.get(0));
                    $dialog
                        .hide()
                        .fadeIn(function () {
                            $dialog.find(".image[tabindex=0]").focus();
                        });
                },
                true
            );
        }

        this.showPreviousImage = function (entry) {
            var $entries = $imageGallery.find(".image_entry");
            var prev = jQuery(entry).prev(".image_entry").get(0)
                    || jQuery(entry).parent().find(".image_entry:last").get(0);
            this.showImage(prev);
        }

        this.showNextImage = function (entry) {
            var $entries = $imageGallery.find(".image_entry");
            var next = jQuery(entry).next(".image_entry").get(0)
                    || jQuery(entry).parent().find(".image_entry").get(0);
            this.showImage(next);
        }

        this.createImageDialog = function (entry) {

            if (!entry) {
                return;
            }

            var $entry = jQuery(entry);
            var imageURL = $entry.find(".image_link").attr("href");
            var imageTitle = $entry.find(".image_label").html();

            var $dialog = jQuery(cocktail.instantiate("woost.views.ImageGallery.image_dialog"));

            $dialog.bind("dialogClosed", function () {
                $dialog = null;
                $entry.find(".image_link").focus();
            });

            $dialog.find(".dialog_content .image").attr("src", imageURL);

            if (imageTitle) {
                $dialog.find(".dialog_heading").html(imageTitle);
            }

            if (singleImage) {
                $dialog.find(".dialog_header .index").hide();
            }
            else {
                $dialog.find(".dialog_header .index").html(
                    ($entry.index() + 1) + " / " + $imageGallery.find(".image_entry").length
                );
            }

            var $entryFootnote = $entry.find(".image_footnote");
            if ($entryFootnote.length) {
                $dialog.find(".footnote").html($entryFootnote.html());
            }
            else {
                $dialog.find(".footnote").hide();
            }

            if (entry.originalImage) {
                var $originalLink = $dialog.find(".original_image_link");
                $originalLink.find("a").attr("href", entry.originalImage);
                $originalLink.show();
            }
            else {
                $dialog.find(".original_image_link").hide();
            }

            var $close = $dialog.find(".close_button");
            var $next = $dialog.find(".next_button");
            var $prev = $dialog.find(".previous_button");
            var $img = $dialog.find(".image");
            var $dialogControls = jQuery().add($next).add($prev);

            // Close dialog button
            $close.click(cocktail.closeDialog);

            // Image cycling
            if (singleImage) {
                $next.hide();
                $prev.hide();
                $img.attr("tabindex", "-1");
            }
            else {
                // Next button
                $next.click(function () {
                    $imageGallery.get(0).showNextImage(entry);
                });

                // Previous button
                $prev.click(function () {
                    $imageGallery.get(0).showPreviousImage(entry);
                });

                $img
                    // Keyboard controls
                    .attr("tabindex", "0")
                    .keydown(function (e) {
                        // Right: show next image
                        if (e.keyCode == 39) {
                            $imageGallery.get(0).showNextImage(entry);
                            return false;
                        }
                        // Left: show previous image
                        else if (e.keyCode == 37) {
                            $imageGallery.get(0).showPreviousImage(entry);
                            return false;
                        }
                        // Home: show first image
                        else if (e.keyCode == 36) {
                            $imageGallery.get(0).showImage($imageGallery.find(".image_entry").get(0));
                            return false;
                        }
                        // End: show last image
                        else if (e.keyCode == 35) {
                            $imageGallery.get(0).showImage($imageGallery.find(".image_entry").last().get(0));
                            return false;
                        }
                    })
                    // Click the image to show the next image
                    .click(function () {
                        $imageGallery.get(0).showNextImage(entry);
                    });

                    // Only show dialog controls when hovering over the image
                    $dialog.hover(
                        function () { $dialogControls.show(); },
                        function () { $dialogControls.hide(); }
                    );
            }

            return $dialog.get(0);
        }

        // Image pre-loading
        if (this.closeUpPreload) {
            $imageGallery.find(".image_entry .image_link").each(function () {
                $imageGallery.get(0).loadImage(this.href);
            });
        }
    },
    children: {
        ".image_entry": function ($entry, $imageGallery) {

            var $link = $entry.find(".image_link");

            $link.click(function () {
                $imageGallery.get(0).showImage($entry.get(0));
                return false;
            });
        }
    }
});

