define([
  'jquery',
  'pat-registry',
  'pat-base',
  'mockup-patterns-filemanager'
], function($, registry, Base) {
  'use strict';
  // initialize only if we are in top frame
  if (window.parent === window) {
    if (!registry.initialized) {
      registry.init();
    }
  }
});
