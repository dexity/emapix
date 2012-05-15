function initialize() {
var lajolla = new google.maps.LatLng(32.818062,-117.269440);
var myOptions = {
  center: lajolla,
  zoom: 13,
  mapTypeId: google.maps.MapTypeId.ROADMAP
};
var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
var marker = new google.maps.Marker({
    position: lajolla,
    title:"Hello World!"
});
marker.setMap(map);
}
