define([
    'backbone',
    'js/models/AppModel',
    'text!js/views/app/AppTemplate.html',
    'js/views/app/CardView',
    'js/views/LightLoader/LightLoader',
    'js/views/ToggleButtons/ToggleButtonsView'
    ], function(
        Backbone,
        AppModel,
        AppTemplate,
        CardView,
        LightLoader,
        ToggleButtons
        ) {
  var App = Backbone.View.extend({

    template: _.template(AppTemplate),

    model: new AppModel(),

    initialize: function() {
      this.render();
    },

    render: function() {
        var that = this;
        $("#main-content").html(this.template());

        $(document).ajaxStart(function() {
            that.model.set('loading', (new LightLoader({el: "#results"})));
        });

        $(document).ajaxStop(function() {
            if (that.model.get('loading') !== undefined) {
                that.model.get('loading').stahp();
            }
        });

        $("#search-bar").on('input', _.debounce(_.bind(that.handleSearch, that), 300));
        $("#search-bar-form").on('submit', function(e) {
            e.preventDefault();
            that.handleSearch();
        });

        $("#results").on('click', function(e) {
            e.preventDefault();
            if ($(e.target).data('id') !== undefined) {
                that.goTo('/search/' + encodeURIComponent($(e.target).data('id')));
                $("html, body").animate({ scrollTop: 0 }, "slow");
                 return false;
            }
        });

        $("#toggle-btn-container").on('click', function(e) {
            var t = $(e.target);
            if (t.hasClass('toggle-btn')) {
                if (t.children('input').first().is(':checked')) {
                    $(".card-" + t.data('toggle')).parents('.card-container').fadeOut();
                } else {
                    $(".card-" + t.data('toggle')).parents('.card-container').fadeIn();
                }
            }
        });

        // create the search bar - has live update of possible things from api
        // $("#search-bar").select2({
            // placeholder: "Actually Find Things ('CSC 220', 'ENGR')",
            // minimumInputLength: 1,
            // ajax: {
            //     url: 'http://myfoot.org/api',
            //     dataType: 'json',
            //     data: function(q) {

            //         return {
            //             q: q
            //         };
            //     },
            //     quietMillis: 300,
            //     cache: true,
            //     results: function(data) {
            //         return {results: data.values};
            //     }
            // },
            // formatResult: function(obj) {
            //   if (obj.type == "Course") {
            //     return obj.text + " (" + obj.CourseCode + ")";
            //   } else {
            //     return obj.text;
            //   }
            // },
            // formatSelection: function(obj) {
            //   if (obj.type == "Course") {
            //     return obj.text + " (" + obj.CourseCode + ")";
            //   } else {
            //     return obj.text;
            //   }
            // }
        // }).on('change', function(e) {
        //     if (e.added === undefined) {
        //       return;
        //     }

        // });
    },

    handleSearch: function() {
        this.goTo('search/' + encodeURIComponent($("#search-bar").val()));
    },


    fetchData: function() {
        // could do google-like parsing with the colons
        // e.g.
        // classes:CSC 220
        // courses:engineering
        // subjects:College of Engineering
        // etc
        // Professors:Engineering //or "Engineering Professors"
        var that = this;
        this.model.set('search', $("#search-bar").val());
        var q = this.model.get('search');
        if (q === "")
            return;

        $.ajax({
            url: 'http://myfoot.org/api',
            type: 'GET',
            dataType: 'JSON',
            data: {q: q},
            success: function(data) {
                if ($("#light-loader").length !== 0)
                    $("#light-loader").hide();
                $("#results").html("");

                results = _.uniq(data.values);
                // if (results.length == 1) {
                    // show the detail view for the object.
                    // so a department page, list of professors, etc
                    // that.goTo('/search/' + encodeURIComponent(results[0].id));
                    // needs more thought and work
                // } else {
                    _.each(results, function(result) {
                        new CardView({el: "#results", obj: result});
                    });
                // }

                var uniq_types = _.uniq(_.map(results, function(r){return r.type;}));

                // Create a new set of buttons
                toggle_buttons = new ToggleButtons({el: "#toggle-btn-container", uniq_types: uniq_types});
            }

        });


    }

  });

  return App;
});