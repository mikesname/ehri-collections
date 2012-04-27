// 
// Subnav with scrollspy, borrowed from Bootstrap docs.
//

jQuery(function($) {
    // fix sub nav on scroll - this is all
    // nicked from Bootstraps (nice looking) docs and needs
    // to be done properly at some point

    // Wire up body for scrollspy
    $("body").scrollspy({
        offset: 300,
    });

    var $win = $(window)
      , $nav = $('.subnav')
      , navTop = $('.subnav').length && $('.subnav').offset().top - 40
      , isFixed = false;

    processScroll();

    // hack sad times - holdover until rewrite for 2.1
    $nav.on('click', function () {
      if (!isFixed) setTimeout(function () {  $win.scrollTop($win.scrollTop() - 47) }, 100);
    })

    $win.on('scroll', processScroll);

    function processScroll() {
      var i, scrollTop = $win.scrollTop();
      if (scrollTop >= navTop && !isFixed) {
        isFixed = true;
        $nav.addClass('subnav-fixed');
      } else if (scrollTop <= navTop && isFixed) {
        isFixed = false;
        $nav.removeClass('subnav-fixed');
      }
    }
});


