define([
    'backbone'
    ], function(
        Backbone
        ) {
  var Card = Backbone.View.extend({

    initialize: function(options) {
        this.render();
    },

    render: function() {
        if ($("#light-loader").length === 0) {
            $("body").first().append('<img src="/img/loading-sm.gif" id="light-loader">');
        } else {
            $("#light-loader").fadeIn();
        }
    },

    stahp: function() {
        if ($("#light-loader").length === 0)
            $("#light-loader").fadeOut();
    }

  });

  return Card;
});