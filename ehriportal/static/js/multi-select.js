
//
// Turn multiple value selects into
// auto-complete lists. This is stolen
// wholesale from Qubit (with minor adjustments
// to remove Drupally bits.) Kudos to whoever 
// wrote the original, which is nicer than 
// this re-implementation.
//

jQuery(document).ready(function($) {

    $.fn.multiSelect = function(options) {

        function handleOption($option, name, $list) {
            $option.prop("disabled", true);
            $("<li/>")
                .html($option.html())
                .append($("<input type='hidden' name='" + name + "' />")
                        .attr("value", $option.val()))
                .click(function(event) {
                    $(this).hide("fast", function() {
                        $(this).remove();
                        $option.prop("disabled", false);
                        $list.toggle($list.children().length != 0);
                    });
                })
                .appendTo($list.show());
        }

        function handleSelect(select) {
            var $list = $("<ul></ul>");
            $list.hide().insertBefore(select);
            var name = $(select).attr("name");
            $(select)
                .prepend($("<option/>"))
                .removeAttr("name")
                .removeAttr("multiple")
                .bind("blur click keydown", function(event) {
                    // only handle TAB events on keydown
                    if ($(this).val() && (event.type != "keydown" || event.keyCode == 9)) {
                        var $opt = $(this).find("option:selected");
                        event.preventDefault();
                        handleOption($opt, name, $list);
                        $(this).val(null);
                    }
                })
                .find("option:selected").each(function(i, opt) {
                    handleOption($(opt), name, $list);    
                })
                .end()
                .val(null);
        }

        this.each(function(i, elem) {
            handleSelect(elem);
        })
    }
    $("select[multiple]").multiSelect();
});
