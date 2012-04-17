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

    // remove existing inline elements when clicked
    $(document).on("click", ".inlineitem", function(event) {
        $(this).find("input[type='checkbox']")
            .prop("checked", true)
            .end()
            .hide(200);
    });

    // add new inline elements when enter or tab pressed in their input
    $(document).on("keydown", ".inlinemulti > input:visible", function(event) {
        if ($.trim($(this).val()) != "" && (event.keyCode == 9 || event.keyCode == 13)) {
            if (this.id.match(/id_([^\d]+)-(\d+)-[^\d]+/)) {
                event.preventDefault();
                var prefix = RegExp.$1, index = parseInt(RegExp.$2);
                addNewAfter(index, prefix);
                setReadOnly(index, prefix);
            }
        }
    });

    // hide the delete checkboxes
    $("input[id$='-DELETE']").add("label[for$='-DELETE']").hide();

    // add a placeholder to the visible fields.
    $(".inlinemulti > input[type='text]:visible").each(function(i, elem) {
        $(elem).attr("placeholder", "Add New " + $(elem).closest("label").text());
    });

    function setReadOnly(index, prefix) {
        var div = $("#id_form-" + prefix + "-" + index),
            idfield = $("#id_" + prefix + "-" + index + "-id"),
            inputs = idfield.nextUntil("input[type='checkbox']"),
            check = inputs.next("input[type='checkbox']"),
            valstr = inputs.map(function(i, e) { return $(e).val();}).toArray().join(" - ");
        inputs.hide().last().after($("<ul><li>" + valstr + "</li></ul>"));
        div.addClass("inlineitem");
    }

    function addNewAfter(index, prefix) {
        var totalforms = parseInt($("#id_" + prefix + "-TOTAL_FORMS").val()),
            initialforms = parseInt($("#id_" + prefix + "-INITIAL_FORMS").val()),
            div = $("#id_form-" + prefix + "-" + index),
            newdiv = div.clone(),
            newindex = index + 1;
        newdiv
            .attr("id", "id_form-" + prefix + "-" + newindex)
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
        var name = $("#id_formset-" + prefix).find("label").first().text();
        newdiv.find("inputs[type='text']").attr("placeholder", "Add New " + name);
        $("#id_" + prefix + "-TOTAL_FORMS").val(totalforms + 1);
        div.after(newdiv).find("input[type='text']").first().focus();
    }
            
    $(".dynamic-formset").each(function(i, elem) {
        var prefix = $(this).data("prefix"),
            initialforms = parseInt($("#id_" + prefix + "-INITIAL_FORMS").val());
        for (var i = 0; i < initialforms; i++) {
            setReadOnly(i, prefix);
        }
    });
});

