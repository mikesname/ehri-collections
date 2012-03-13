#
# Coffeescript attempt
#

initialize = ->
  ele = document.getElementById("map_canvas")
  $(ele).height $(window).height() - $(ele).position().top - 10
  myOptions =
    center: new google.maps.LatLng(56, 24)
    zoom: 4
    mapTypeId: google.maps.MapTypeId.ROADMAP
  new google.maps.Map(ele, myOptions)

getParameterByName = (url, name) ->
  name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]")
  regexS = "[\\?&]" + name + "=([^&#]*)"
  regex = new RegExp(regexS)
  results = regex.exec(url)
  unless results?
    ""
  else
    decodeURIComponent results[1].replace(/\+/g, " ")

setSearchData = (data, clear) ->
  console.log "" + data.object_list.length + " Results"
  clearSearchData()  if clear

clearSearchData = ->
    #$.each gmarkers, (i, m) ->
        #m.setMap null
  m.setMap null for m in gmarkers
  $("#result-list").html ""

search = (query, type, page) ->
  $.ajax
    url: window.location.pathname
    data:
      q: query
      type: type
      format: "json"
      page: page

    dataType: "json"
    error: ->
      console.error arguments

    success: (data) ->
      result.setFromData data

fitBoundsWithMinimumZoom = (map, bounds, minzoom=10) ->
  zc = google.maps.event.addListener(gmap, "zoom_changed", ->
    bc = google.maps.event.addListener(gmap, "bounds_changed", (event) ->
      @setZoom minzoom  if @getZoom() > minzoom
      google.maps.event.removeListener bc
    )
  )
  map.fitBounds bounds
  google.maps.event.removeListener zc

Repository = Backbone.Model.extend({})

SearchResult = Backbone.Model.extend(
  defaults:
    has_other_pages: false
    has_previous: false
    has_next: false
    page: 1
    total: 0
    object_list: []

  setFromData: (data) ->
    @set
      page: data.page
      total: data.total
      has_next: data.has_next
      has_previous: data.has_previous
      has_other_pages: data.has_other_pages
      object_list: data.object_list
)

SearchListView = Backbone.View.extend(
  initialize: ->
    @model.bind "change", @render, this

  _renderObject: (repo) ->
    url = dutils.urls.resolve("repo_detail",
      slug: repo.slug
    )
    $("#result-list").append "<h4><a class='repo-link' href='" + url + "'>" + repo.name + "</a></h4>"
    gmarkers.push new google.maps.Marker(
      position: new google.maps.LatLng(repo.location[1], repo.location[0])
      map: gmap
      title: repo.name
      data: repo
    )

  render: ->
    list = (repo for repo in @model.get("object_list") when repo.location?)
    clearSearchData()  unless @model.get "has_previous"
    @_renderObject repo for repo in list
    console.log "List", list
    if list.length
      bounds = new google.maps.LatLngBounds()
      bounds.extend m.position for m in gmarkers
      fitBoundsWithMinimumZoom gmap, bounds
)

gmap = undefined
gmarkers = []
result = undefined
listview = undefined

jQuery ->
  gmap = initialize()
  result = new SearchResult()
  listview = new SearchListView(model: result)

  window.onpopstate = (event) ->
    $("#id_q").val getParameterByName window.location.search, "q"
    $("#search-form").submit()

  $("#search-form").submit (event) ->
    val = $("#id_q").val()
    type = $("#id_type").val()
    window.history.pushState
      q: val
    , window.title, window.location.pathname + "?" + $(this).serialize()
    search val, type
    event.preventDefault()

