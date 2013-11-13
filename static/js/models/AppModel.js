define(['backbone'], function(Backbone) {
    var AppModel = Backbone.Model.extend({
        defaults: {
            'search': '',
            'history': []
        }
    });
    return AppModel;
});