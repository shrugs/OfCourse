define(['backbone'], function(Backbone) {
    var CardModel = Backbone.Model.extend({
        defaults: {
            'title': 'Default Title',
            'detail': 'Default Detail Text',
            'obj': {}
        }
    });
    return CardModel;
});