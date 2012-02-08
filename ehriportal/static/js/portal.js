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


    var slider = $('.slide-out-div').tabSlideOut({
        tabHandle: '.handle',                              
        pathToTabImage: '/site_media/static/img/feedback_tab.png',          
        imageHeight: '75px',                               
        imageWidth: '24px',                               
        tabLocation: 'left',                               
        speed: 300,                                        
        action: 'click',                                   
        topPos: '50px',                                   
        fixedPosition: true,
        onSlideOut: function() {
        },
        onSlideIn: function() {
        },
    });

    // handle suggestion form submission... this is a bit
    // gross and fragile.
    var emailregexp = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    $("#id_suggestion-name, #id_suggestion-text").keyup(function(event) {
        var name = $.trim($("#id_suggestion-name").val());
        var text = $.trim($("#id_suggestion-text").val());
        var email = $.trim($("#id_suggestion-email").val());
        // email is not reqired, so only check it if filled in
        var emailvalid = email !== "" && email.match(emailregexp);
        var ok = name !== "" && text !== "" && emailvalid;
        $("#submit-suggestion").prop("disabled", !ok);
    });

    $("#suggestions-form").find(".modal-close").click(function() {
        $(".slide-out-div > .handle").click(); 
    });

    $("#submit-suggestion").click(function(event) {
        event.preventDefault();
        var form = $(this).closest("form");
        $.post(form.attr("action"), form.serialize(), function(data, textStatus) {
            // FIXME: This is rubbish.
            var thanks = $("#suggestion-thanks");            
            thanks.width(thanks.parent().width() - (thanks.outerWidth(true) - thanks.width()));
            thanks.slideDown(500, function() {
                setTimeout(function() {
                    $(".slide-out-div > .handle").click();
                    $("#id_suggestion-text").val("");
                    thanks.slideUp(500); 
                }, 1000);
            });
        });
    });
});
