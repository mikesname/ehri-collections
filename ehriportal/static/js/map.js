(function() {
  var SearchListView, SearchResult, SummaryView, clearSearchData, fitBoundsWithMinimumZoom, getParameterByName, gmap, gmarkers, initialize, listview, result, setSearchData;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  initialize = function() {
    var ele, myOptions;
    ele = document.getElementById("map_canvas");
    $(ele).height($(window).height() - $(ele).position().top - 10);
    myOptions = {
      center: new google.maps.LatLng(56, 24),
      zoom: 4,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    return new google.maps.Map(ele, myOptions);
  };
  getParameterByName = function(url, name) {
    var regex, regexS, results;
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    regexS = "[\\?&]" + name + "=([^&#]*)";
    regex = new RegExp(regexS);
    results = regex.exec(url);
    if (results == null) {
      return "";
    } else {
      return decodeURIComponent(results[1].replace(/\+/g, " "));
    }
  };
  setSearchData = function(data, clear) {
    console.log("" + data.object_list.length + " Results");
    if (clear) {
      return clearSearchData();
    }
  };
  clearSearchData = function() {
    var m, _i, _len;
    for (_i = 0, _len = gmarkers.length; _i < _len; _i++) {
      m = gmarkers[_i];
      m.setMap(null);
    }
    return $("#result-list").html("");
  };
  fitBoundsWithMinimumZoom = function(map, bounds, minzoom) {
    var zc;
    if (minzoom == null) {
      minzoom = 10;
    }
    zc = google.maps.event.addListener(gmap, "zoom_changed", function() {
      var bc;
      return bc = google.maps.event.addListener(gmap, "bounds_changed", function(event) {
        if (this.getZoom() > minzoom) {
          this.setZoom(minzoom);
        }
        return google.maps.event.removeListener(bc);
      });
    });
    map.fitBounds(bounds);
    return google.maps.event.removeListener(zc);
  };
  SearchResult = Backbone.Model.extend({
    defaults: {
      query: "",
      has_other_pages: false,
      has_previous: false,
      has_next: false,
      page: 1,
      total: 0,
      object_list: []
    },
    setFromData: function(query, data) {
      return this.set({
        page: data.page,
        total: data.total,
        has_next: data.has_next,
        has_previous: data.has_previous,
        has_other_pages: data.has_other_pages,
        object_list: data.object_list,
        query: query
      });
    },
    search: function(query, type, page) {
      return $.ajax({
        url: window.location.pathname,
        data: {
          q: query,
          type: type,
          format: "json",
          page: page
        },
        dataType: "json",
        error: function() {
          return console.error(arguments);
        },
        success: __bind(function(data) {
          return this.setFromData(query, data);
        }, this)
      });
    },
    totalWithLocations: function() {
      var repo, _i, _len, _ref, _results;
      _ref = this.get("object_list");
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        repo = _ref[_i];
        if (repo.location != null) {
          _results.push(repo);
        }
      }
      return _results;
    }
  });
  SearchListView = Backbone.View.extend({
    initialize: function() {
      return this.model.bind("change", this.render, this);
    },
    _renderObject: function(repo) {
      var url;
      url = dutils.urls.resolve("repo_detail", {
        slug: repo.slug
      });
      this.$el.append("<h4><a class='repo-link' href='" + url + "'>" + repo.name + "</a></h4>");
      return gmarkers.push(new google.maps.Marker({
        position: new google.maps.LatLng(repo.location[1], repo.location[0]),
        map: gmap,
        title: repo.name,
        data: repo
      }));
    },
    render: function() {
      var bounds, list, m, query, repo, _i, _j, _len, _len2;
      list = this.model.totalWithLocations();
      query = this.model.get("query");
      if (!this.model.get("has_previous")) {
        clearSearchData();
      }
      console.log("rendering");
      if (list.length) {
        for (_i = 0, _len = list.length; _i < _len; _i++) {
          repo = list[_i];
          this._renderObject(repo);
        }
        bounds = new google.maps.LatLngBounds();
        for (_j = 0, _len2 = gmarkers.length; _j < _len2; _j++) {
          m = gmarkers[_j];
          bounds.extend(m.position);
        }
        return fitBoundsWithMinimumZoom(gmap, bounds);
      }
    }
  });
  SummaryView = Backbone.View.extend({
    initialize: function() {
      return this.model.bind("change", this.render, this);
    },
    render: function() {
      var count, query, summary;
      count = this.model.totalWithLocations().length;
      query = this.model.get("query");
      if (query === "") {
        summary = "";
      } else {
        summary = !count ? "Nothing found for <i>" + query + "</i>" : "" + count + " Result" + (count !== 1 ? "s" : "") + " for <i>" + query + "</i>";
      }
      return this.$el.html(summary);
    }
  });
  gmap = void 0;
  gmarkers = [];
  result = void 0;
  listview = void 0;
  jQuery(function() {
    var sumview;
    gmap = initialize();
    result = new SearchResult();
    listview = new SearchListView({
      model: result,
      el: "#result-list"
    });
    sumview = new SummaryView({
      model: result,
      el: "#result-summary"
    });
    window.onpopstate = function(event) {
      $("#id_q").val(getParameterByName(window.location.search, "q"));
      return $("#search-form").submit();
    };
    return $("#search-form").submit(function(event) {
      var type, val;
      val = $("#id_q").val();
      type = $("#id_type").val();
      window.history.pushState({
        q: val
      }, window.title, window.location.pathname + "?" + $(this).serialize());
      result.search(val, type);
      return event.preventDefault();
    });
  });
}).call(this);
