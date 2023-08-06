(function($) {
  "use strict";
  $(document).ready(function() {
    var overlay_set = false;
    $('.calltoaction-portlet-wrapper').each( function() {
      // Check if the user has already seen this overlay.
      var cookiename = $(this).attr('data-cookiename');
      // Note: readCookie and createCookie are defined in
      // Products/CMFPlone/skins/plone_ecmascript/cookie_functions.js
      if (!overlay_set && !readCookie(cookiename)) {
        var timeout = $(this).attr('data-timeout');
        var el = $(this);
        setTimeout(
          function(){
            // Overlay adapted from http://jquerytools.github.io/demos/overlay/trigger.html
            el.overlay({
              // custom top position
              top: "center",
              fixed: true,
              // Before the overlay is gone be active place it correctly 
              onBeforeLoad: function() {

                if (el.hasClass("manager_right")){
                  el.animate({right: -1000});
                }else{
                  el.animate({left: -1000});
                };

              },
              // when the overlay is opened, animate our portlet
              onLoad: function() {

                if (el.hasClass("manager_right")){
                   el.animate({right: 15});
                } 
                else {
                    el.animate({left: 15});
                };

              },
              // some mask tweaks suitable for facebox-looking dialogs
              mask: {
                // you might also consider a "transparent" color for the mask
                color: '#fff',
                // load mask a little faster
                loadSpeed: 200,
                // very transparent
                opacity: 0.5
              },
              // disable this for modal dialog-type of overlays
              closeOnClick: true,
              // load it immediately after the construction
              load: true,

            });
            
            // Set cookie to avoid showing overlay twice to the same
            // user.  We could do this on certain events, but you have
            // to catch them all: onClose of the overlay, clicking on
            // a link in the overlay, etcetera.  Much easier to simply
            // set the cookie at the moment we show the overlay.
            createCookie(cookiename, 'y', 365);
          },
          timeout);
        // We setup only one overlay, otherwise it gets a bit crazy.
        overlay_set = true;
      };
    });
  });
})(jQuery);
