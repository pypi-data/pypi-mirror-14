/* RequireJS configuration */
/* global module:true */

(function() {
  'use strict';

  var requirejsOptions = {
    baseUrl: './',
    optimize: 'none',
    paths: {
      'highlightjs': 'bower_components/highlightjs/highlight.pack',
      'pat-highlightjs': 'bower_components/pat-highlightjs/src/pat-highlightjs',

      'mockup-bundles-highlightjs': 'js/bundles/highlightjs',

      // FRAMEWORK DEPENDENCIES
      'expect': 'bower_components/expect/index',
      'jquery': 'bower_components/jquery/dist/jquery',
      'jquery.browser': 'bower_components/jquery.browser/dist/jquery.browser',
      'logging': 'bower_components/logging/src/logging',
      'pat-base': 'bower_components/patternslib/src/core/base',
      'pat-compat': 'bower_components/patternslib/src/core/compat',
      'pat-jquery-ext': 'bower_components/patternslib/src/core/jquery-ext',
      'pat-logger': 'bower_components/patternslib/src/core/logger',
      'pat-mockup-parser': 'bower_components/patternslib/src/core/mockup-parser',
      'pat-registry': 'bower_components/patternslib/src/core/registry',
      'pat-utils': 'bower_components/patternslib/src/core/utils',
      'underscore': 'bower_components/underscore/underscore'
    }
  };

  if (typeof exports !== 'undefined' && typeof module !== 'undefined') {
    module.exports = requirejsOptions;
  }
  if (typeof requirejs !== 'undefined' && requirejs.config) {
    requirejs.config(requirejsOptions);
  }

}());
