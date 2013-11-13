define(['backbone', 'js/views/app/AppView'], function(Backbone, App) {
    return Backbone.Router.extend({

        initialize: function() {
            this.app = new App();
        },

        routes: {
            '': 'home',
            'class/:ClassID': 'ClassID',
            'search/:search' : 'makeSearch'
        },

        home: function() {
            this.app.handleSearch();
        },

        ClassID: function(id) {
            console.log(id);
        },

        makeSearch: function(q) {
            $("#search-bar").val(q);
            this.app.fetchData();
        }


    });
});