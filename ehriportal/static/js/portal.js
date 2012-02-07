$(function($) {

    $(".more-facets").each(function(i, elem) {
        $(elem).modal({backdrop:true,
            shown: function(e) { alert("show"); },
        });
    });

    // add Ajax behaviour on pagination links
    $(".ajax, .modal-body > .pagination ul li a").live("click", function(event) {
        // MASSIVE HACK - extract the facet class from the fclass data attribute
        // that is written into the modal-body div and alter the various
        // links to point the the particular facet list page.  This is deeply
        // offensive to all that is good and pure...
        var klass = $(".modal-body").data("fclass");
        if (klass && this.href) {
            event.preventDefault();
            $("#modal-popup").load(this.href.replace(/search\?/, "search/" + klass + "/?"));
        }
    });

    $(".facet-header").click(function(event) {
        event.preventDefault();
        $(this).parent().next("dl").toggle(200);
    });

});
