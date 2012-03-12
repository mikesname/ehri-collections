var Repository = Backbone.Model.extend({
});

var SearchResult = Backbone.Model.extend({
    defaults: {
        has_other_pages: false,
        has_previous: false,
        has_next: false,
        page: 1,
        total: 0,
        object_list: [],
    },

    setFromData: function(data) {
        this.set({
            page: data.page,
            total: data.total,
            has_next: data.has_next,
            has_previous: data.has_previous,
            has_other_pages: data.has_other_pages,
            object_list: data.object_list,
        });    
    },
});

var SearchListView = Backbone.View.extend({
    initialize: function() {
        this.model.bind("change", this.render, this);    
    },

    _renderObject: function(repo) {
        var url = dutils.urls.resolve('repo_detail', {slug: repo.slug});
        $("#result-list").append(
            "<h4><a class='repo-link' href='" + url + "'>" + repo.name +
                    "</a></h4>");
        gmarkers.push(new google.maps.Marker({
            position: new google.maps.LatLng(repo.location[1],
                          repo.location[0]),
            map: gmap,
            title: repo.name,
            data: repo,
        }));    
    },

    render: function() {
        console.log("rendering", this.model);
        var self = this;
        var list = this.model.get("object_list");
        var prev = this.model.get("has_previous");
        if (!prev)
            clearSearchData();
        if (list) {
            $.each(this.model.get("object_list"), function(i, repo) {
                if (repo.location) {
                    self._renderObject(repo);
                }
            });
        }
    },
});

var result = new SearchResult();
var listview = new SearchListView({model:result});


function initialize() {
    var ele = document.getElementById("map_canvas");
    $(ele).height($(window).height() - $(ele).position().top - 10);
    var myOptions = {
        center: new google.maps.LatLng(56, 24),
        zoom: 4,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    return new google.maps.Map(ele, myOptions);
}

function getParameterByName(url, name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(url);
    if(results == null)
        return "";
    else
        return decodeURIComponent(results[1].replace(/\+/g, " "));
}

function setSearchData(data, clear) {
    console.log("" + data.object_list.length + " Results");
    if (clear)
        clearSearchData();
}

function clearSearchData() {
    $.each(gmarkers, function(i, m) { m.setMap(null);});
    $("#result-list").html("");
}

function search(query, type, sw, ne, page) {
    // fetch the data
    $.ajax({
        url: window.location.pathname,
        data: {q: query, type: type, format: "json", ne: ne, sw: sw, page: page},
        dataType: "json",
        error: function() {
            console.error(arguments);
        },
        success: function(data) {
            result.setFromData(data);
        },
    });
}

var gmap, gmarkers = [];
$(function() {
    gmap = initialize();

    // set sidebar height
    var ele = document.getElementById("result-list");
    $(ele)
        .css({overflow: "auto"})
        .height($(window).height() - $(ele).position().top - 10);


    window.onpopstate = function(event) {
        $("#id_q").val(getParameterByName(window.location.search, "q"));
        $("#search-form").submit();
    };

    //$("#map_canvas").bind("mousedown.dragmap", function(event) {
    //    var mapele = this;
    //    var boundsstart = gmap.getBounds();
    //    $(this).bind("mouseup.dragmap", function(uevent) {
    //        var boundsend = gmap.getBounds();
    //        if (boundsstart != boundsend) {
    //            $("#search-form").submit();
    //            $(mapele).unbind("mouseup.dragmap");
    //        }
    //    });
    //});

    $("#search-form").submit(function(event) {
        var val = $("#id_q").val(),
            type = $("#id_type").val(),
            ne =  gmap.getBounds().getNorthEast().toUrlValue(),
            sw = gmap.getBounds().getSouthWest().toUrlValue();

        // fix the browser URL
        window.history.pushState({q:val}, window.title, 
            window.location.pathname + "?" + $(this).serialize());

        search(val, type, sw, ne);
        event.preventDefault();        
    });
});

