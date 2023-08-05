/**
 * ImageType renderer<br>
 * It compiles all <control_date> tags that have been inserted into HTML, and turns them into <input type="text">s<br>
 *
 * @author  Fabio Pavesi (fabio@adamassoft.it)
 * @namespace
 */
var ImageType = (function() {
    /**
     *
     * @memberOf Textbox
     */
    function render() {
        var control;
        $("control_image").each(function() {
            var temp = edi.getTempStructure()[$(this).attr("id")];
            var element = temp.element;
            var item = temp.item;

            if ( item.hasDatatype == "text" ) {
                control = $.parseHTML("<textarea class='" + defaults.controlCSS + " " + item.hasDatatype + "-input'>");
            } else {
                control = $.parseHTML("<input type='text' class='" + defaults.controlCSS + " " + item.hasDatatype + "-input'>");
            }
            if ( item.show == "hidden" || item.hasDatatype == "autonumber" ) {
                $(control).attr("type", "hidden");
            }
            var theElement = ediml.getElement(element.id);
            var theItem = new Item();
            theItem.id = item.id;

            ItemRenderer.copyAttributesFrom(element, item, theItem);

            theElement.addItem(theItem);

            control = $(control);

            control.attr("datatype", item.hasDatatype);
            control.attr("datasource", item.datasource);
            control.attr("show", item.show);
            control.attr("id", $(this).attr("id"));
            control.attr("defaultValue", item.defaultValue);
            control.attr("field", item.field);
            control.attr("querystringparameter", item.queryStringParameter);
            if (item.isFixed == "true") {
                control.val(item.hasValue);
                control.addClass("fixed");
            }
            if (element.isMandatory != "NA") {
                control.attr("required", "required");
            }
            control.change(function() {
                var div = $("#image_" + $(this).attr("id"));
                div.html("<img src='" + $(this).val() + "'>");
            });
            var html = $.parseHTML("<div class='" + defaults.controlGroupCSS + " col-md-12" + ( item.hasDatatype == "date" ? " date" : "" ) + "'>");
            html = $(html);
            var labels = $(this).find("label, helps");
            $(labels).addClass(defaults.labelCSS);
            console.log(labels);
            if ( item.show != "hidden" ) {
                html.append(labels);
            }
            html.append(control);
            html.append("<div id='image_" + $(this).attr("id") + "' class='url_thumb'>");
            $(this).replaceWith(html);
            /*
             if (item.hasDatatype == "copy") {
             console.log(item.id);
             $("#" + item.itemId).change(function (event) {
             console.log(event + " received");
             $("#" + item.id).val($(this).val()).trigger("change");
             });
             }
             */

        });
    }
    return {
        render: render
    };

})();