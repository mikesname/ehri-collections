$(function($) {

    $(".more-facets").each(function(i, elem) {
        $(elem).modal({backdrop:true,
            shown: function(e) { alert("show"); },
        });
    });

    // add Ajax behaviour on pagination links
    $(".ajax, #facet-popup > .pagination ul li a").live("click", function(event) {
        // MASSIVE HACK - extract the facet class from the fclass data attribute
        // that is written into the modal-body div and alter the various
        // links to point the the particular facet list page.  This is deeply
        // offensive to all that is good and pure...
        var klass = $("#facet-popup").data("fclass");
        if (klass && this.href) {
            event.preventDefault();
            $("#modal-popup").load(this.href.replace(/search\?/, "search/" + klass + "/?"));
        }
    });

    $(".facet-header").click(function(event) {
        event.preventDefault();
        $(this).parent().next("dl").toggle(200);
    });

    // OpenID buttons
    $("a.openid-button").click(function(event) {
        event.preventDefault();
        $("input[name='openid_url']").val(this.href).closest("form").submit();
    });

    // Make sure no more than two revision diff checkboxes are
    // checked at the same time
    $("input[type='submit']", $(".object-version-history")).prop("disabled", true);
    $("input[type='checkbox']", $(".object-version-history")).click(function(event) {        
        var checked = $("input[type='checkbox']:checked", $(".object-version-history"));
        if (checked.length > 2) {
            checked.not(this).prop("checked", false);
        }
        $("input[type='submit']", $(".object-version-history")).prop(
                "disabled", checked.length != 2);
    });

    var slider = $('.slide-out-div').tabSlideOut({
        tabHandle: '.handle',                              
        pathToTabImage: TAB_PATH, 
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

    // Wire up 
    $("body").each(function() {
        var $spy = $(this).scrollspy({
            offset: 100,
            activate: function() {
                console.log(arguments);
            }    
        });
    });
        // fix sub nav on scroll
    var $win = $(window)
      , $nav = $('.subnav')
      , navTop = $('.subnav').length && $('.subnav').offset().top - 40
      , isFixed = 0;

    processScroll();

    // hack sad times - holdover until rewrite for 2.1
    //$nav.on('click', function () {
    //  if (!isFixed) setTimeout(function () {  $win.scrollTop($win.scrollTop() - 47) }, 10)
    //})

    $win.on('scroll', processScroll);

    function processScroll() {
      var i, scrollTop = $win.scrollTop();
      if (scrollTop >= navTop && !isFixed) {
        isFixed = 1;
        $nav.addClass('subnav-fixed');
      } else if (scrollTop <= navTop && isFixed) {
        isFixed = 0;
        $nav.removeClass('subnav-fixed');
      }
    }



    // handle suggestion form submission... this is a bit
    // gross and fragile.
    var form = $("#suggestion-form"),
        submit = $("button[type='submit']", form),
        thanks = $(".alert-success", form),
        name = $("#id_suggestion-name", form),
        text = $("#id_suggestion-text", form),
        email = $("#id_suggestion-email", form),
        emailregexp = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

    name.add(text).add(email).keyup(function(event) {
        var nameval = $.trim(name.val());
        var textval = $.trim(text.val());
        var emailval = $.trim(email.val());
        // email is not reqired, so only check it if filled in
        var emailvalid = (emailval === "" || emailval !== "" && emailval.match(emailregexp));
        var ok = nameval !== "" && textval !== "" && emailvalid;
        submit.prop("disabled", !ok);
    });

    $(".modal-close", form).click(function() {
        $(".slide-out-div > .handle").click(); 
    });

    submit.prop("disabled", true).click(function(event) {
        event.preventDefault();
        submit.prop("disabled", true);
        var formele = $(this).closest("form");
        $.post(formele.attr("action"), formele.serialize(), function(data, textStatus) {
            // FIXME: This is rubbish.
            thanks.width(thanks.parent().width() - (thanks.outerWidth(true) - thanks.width()));
            thanks.slideDown(500, function() {
                setTimeout(function() {
                    $(".slide-out-div > .handle").click();
                    text.val("");
                    thanks.slideUp(500); 
                }, 1000);
            });
        });
    });
});
