require.config({
    appDir: '.',
  paths: {
    'jquery': '//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min',
    'underscore': '//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.4.4/underscore-min',
    'backbone': '//cdnjs.cloudflare.com/ajax/libs/backbone.js/1.0.0/backbone-min',
    'bootstrap': '//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min',
    'text': 'js/text'
  },
  shim: {
    'bootstrap': {
        deps: ['jquery']
    },
    'underscore': {
        exports: '_'
    },
    'backbone': {
        deps: ['underscore', 'jquery'],
        exports: "Backbone"
    }
  }
});

require(['jquery', 'underscore', 'backbone', 'bootstrap', 'js/OfCourseRouter', 'js/views/app/AppView'], function($, _, Backbone, bootstrap, OfCourseRouter, App) {
  var router = new OfCourseRouter();
  // Extend the View class to include a navigation method goTo
  Backbone.View.prototype.goTo = function (loc) {
    router.navigate(loc, true);
  };
  Backbone.history.start();
});