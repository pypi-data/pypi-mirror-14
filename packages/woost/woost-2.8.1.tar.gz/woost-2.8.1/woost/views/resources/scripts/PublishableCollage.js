/*-----------------------------------------------------------------------------


@author:        Martí Congost
@contact:       marti.congost@whads.com
@organization:  Whads/Accent SL
@since:         May 2015
-----------------------------------------------------------------------------*/

cocktail.bind(".PublishableCollage", function ($collage) {

    cocktail.collage.init(this, this.collage);

    var baseSetTileSize = this.collage.layout.setTileSize;
    this.collage.layout.setTileSize = function (tile) {
        var $publishableView = jQuery(tile.content).find(".publishable_view").first();
        if ($publishableView.length && $publishableView[0].setSize) {
            $publishableView[0].setSize(tile.width, tile.height);
        }
        else {
            baseSetTileSize.call(this, tile);
        }
    }
});

