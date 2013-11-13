define([
    'backbone',
    'js/models/CardModel',
    'text!js/views/app/CardTemplate.html'
    ], function(
        Backbone,
        CardModel,
        CardTemplate
        ) {
  var Card = Backbone.View.extend({

    template: _.template(CardTemplate),

    model: new CardModel(),

    initialize: function(options) {
        this.model.set('obj', options.obj);
        this.options.$el = $(options.el);
        this.render();
    },

    render: function() {
        var options = this.model.get('obj');
        options.title = options.text;
        this.options.$el.append(this.template(options));
    }

  });

  return Card;
});