/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			October 2008
-----------------------------------------------------------------------------*/

cocktail.declare("woost.richTextEditor");

woost.richTextEditor.badTags = /^(acronym|applet|basefont|big|center|dir|font|frame|frameset|isindex|noframes|script|tt)$/i;
woost.richTextEditor.badAttributes = /^(style|align|valign|link|alink|vlink|text|background|bgcolor|border|cellpadding|cellspacing|marginheight|marginwidth|nowrap|rules|scrolling|type|frameborder|on.+|data-.+)$/i;

woost.richTextEditor.init = function (editor) {

    function cleanDOM(node) {
        if (node.nodeType == 1) {
            if (woost.richTextEditor.badTags.test(node.tagName)) {
                if (node.parentNode) {
                    node.parentNode.removeChild(node);
                }
                else {
                    node.tagName = "div";
                }
            }
            else {
                for (var a = node.attributes.length - 1; a >= 0; a--) {
                    var name = node.attributes[a].nodeName;
                    if (woost.richTextEditor.badAttributes.test(name)) {
                        node.removeAttribute(name);
                    }
                }
                for (var c = node.childNodes.length - 1; c >= 0; c--) {
                    cleanDOM(node.childNodes[c]);
                }
            }
        }
    }

    editor.on("PastePostProcess", function (e) {
        cleanDOM(e.node);
    });
}

