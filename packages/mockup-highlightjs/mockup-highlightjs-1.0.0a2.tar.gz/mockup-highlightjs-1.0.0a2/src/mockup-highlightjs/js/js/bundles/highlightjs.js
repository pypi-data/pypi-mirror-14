require([
  'jquery',  // We use jquery to search the DOM for pattern declarations.
  'pat-registry',  // We have to register
  'pat-highlightjs'  // Depend on the patterns, you want to support in this bundle.
], function($, Registry) {
  'use strict';

  if (window.parent === window) {
    $(document).ready(function() {
      if (!Registry.initialized) {
        Registry.init();
      }
    });
  }

});
