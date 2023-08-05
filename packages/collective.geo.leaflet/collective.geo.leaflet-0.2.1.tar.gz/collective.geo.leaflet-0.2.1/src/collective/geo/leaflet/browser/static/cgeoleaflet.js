var baselayers = {};
var overlayMaps = {};
var map;
var mapcenter_longitude = $('#map').data('mapcenter_longitude');
var mapcenter_latitude = $('#map').data('mapcenter_latitude');
var coord_type = $('#map').data('coordinates')[0];
var coord_value = $('#map').data('coordinates')[1];
var marker_url = $('#map').data('marker_image');
var zoom = $('#map').data('zoom');
map = new L.Map('map').setView([mapcenter_latitude, mapcenter_longitude], zoom);

$(document).ready(function() {

});
