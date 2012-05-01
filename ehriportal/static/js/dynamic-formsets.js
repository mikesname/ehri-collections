//
// Unobtrusively enhance inline formsets so that adding and
// removing items is prettier and more intuitive.
// Existing items are rendered as a read-only list. List
// items are clicked to remove them.  New items are added
// with a form control, which when confirmed (using enter
// or tab) render themselves as list items.
// NB: This system is very much stolen from ICA-AtoM, which
// probably stole it from Drupal.
//

jQuery(document).ready(function($) {

    // hide the delete checkboxes
    $("input[id$='-DELETE']", ".inlinemulti")
        .add("label[for$='-DELETE']", ".inlinemulti").hide();

    // remove existing inline elements when clicked
    $(document).on("click", ".inline-proxy", function(event) {
        $(this).parent().find("input[type='checkbox']")
            .prop("checked", true)
            .end()
            .hide(200);
    });

    // add new inline elements when enter or tab pressed in their input
    $(document).on("keydown", ".inlinemulti > input[type='text']:visible", function(event) {
        // check if there's another text value in this set. If there is move to
        // it. If not, confirm this control and make a new input
        if ($.trim($(this).val()) != "" && (event.keyCode == 9 || event.keyCode == 13)) {
            var next = $(this).next("input[type='text']").first();
            if (next.length == 0 && this.id.match(/id_([^\d]+)-(\d+)-[^\d]+/)) {
                event.preventDefault();
                var prefix = RegExp.$1, index = parseInt(RegExp.$2);
                addNewAfter(prefix, index);
                setReadOnly(prefix, index);
            }
        }
    });

    function setReadOnly(prefix, index) {
        var div = $("#" + prefix + "-" + index);
        var vals = [];
        div.find("input[type='text']").each(function(i, elem) {
            $(elem).prop("type", "hidden");
            vals.push($(elem).val());
        });
        $("<div></div>").addClass("inline-proxy").text(vals.join(" - ")).appendTo(div);
    }

    function addNewAfter(prefix, index) {
        var totalforms = parseInt($("#id_" + prefix + "-TOTAL_FORMS").val()),
            initialforms = parseInt($("#id_" + prefix + "-INITIAL_FORMS").val()),
            div = $("#" + prefix + "-" + index),
            newdiv = div.clone(),
            newindex = index + 1;
        newdiv
            .attr("id", prefix + "-" + newindex)
            .data("prefix", prefix + "-" + newindex)
            .find("input").val(null);
        newdiv.find("label, input").each(function(i, elem) {
            $.each(["id", "name", "for"], function(i, attr) {
                if ($(elem).attr(attr)) {
                    $(elem).attr(attr, $(elem).attr(attr).replace(
                            prefix + "-" + index, prefix + "-" + newindex));
                }
            });
        });
        $("#id_" + prefix + "-TOTAL_FORMS").val(totalforms + 1);
        newdiv.insertAfter(div).find("input[type='text']").first().focus();
    }

    $(".dynamic-formset").each(function(i, elem) {
        var prefix = $(this).data("prefix"),
            initialforms = parseInt($("#id_" + prefix + "-INITIAL_FORMS").val());
        for (var i = 0; i < initialforms; i++) {
            setReadOnly(prefix, i);
        }
    });
})

