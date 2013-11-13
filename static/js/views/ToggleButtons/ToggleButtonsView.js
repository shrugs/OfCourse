define([
    'backbone',
    'text!js/views/ToggleButtons/ToggleButtonsTemplate.html'
    ], function(
        Backbone,
        ToggleButtonsTemplate
        ) {
  var ToggleButonsView = Backbone.View.extend({

    template: _.template(ToggleButtonsTemplate),

    initialize: function(options) {
        this.options.$el = $(options.el);
        this.options.uniq_types = options.uniq_types;
        this.render();
    },

    render: function() {
        this.options.$el.html(this.template(this.options));
        _.each(this.options.uniq_types, function(t) {
            $("#toggle-btn-" + t.toLowerCase() + "s").button('toggle');
        });
    }

  });

  return ToggleButonsView;
});