
var map;
var infoWindow;
var markersArray;
var pressTimer;

// XXX: Implement long click

String.prototype.format = function() {
	  var args = arguments;
	  return this.replace(/{(\d+)}/g, function(match, number) { 
	    return typeof args[number] != 'undefined'
	      ? args[number]
	      : match
	    ;
	  });
	};

var reqStr		= 'Location: {0}; {1}<br/>' +
	'<button type="button" id="send_request">Send Request</button><br/>';
	
var actionStr	= 'Location: {0}; {1}<br/>' +
	'<button type="button">Take Picture</button><br/>' +
	'<button type="button">Select Picture</button><br/>' +
	'<button type="button">Remove Marker</button><br/>';
	
var previewStr	= '<img src="https://s3.amazonaws.com/emapix_uploads/{0}.jpg" width=200/><br/>' +
	'<button type="button">Submit Picture</button><br/>' +
	'<button type="button">Take Picture</button><br/>' +
	'<button type="button">Remove Marker</button><br/>';
	
var viewStr		= '<img src="https://s3.amazonaws.com/emapix_uploads/{0}.jpg" width=200/><br/>' +
'<button type="button">Remove</button>';

function getMarkers() {
	$.get("http://localhost/api/all", {"key": "0dae2799bb2d9b88e1d38a337377b221"},
			function(data) { 
				var res	= $.parseJSON(data);
				var reqs	= res["result"];
				for (i=0; i<reqs.length; i++) {
					req	= reqs[i];
					lat	= req["lat"]/1e6;
					lon	= req["lon"]/1e6;
					var marker = new google.maps.Marker({
					    position:  	new google.maps.LatLng(lat, lon),
					    title:		req["resource"],
					    map:		map
					    });	
					google.maps.event.addListener(marker, 'click', function() {
							infoWindow.setContent(viewStr.format(req["resource"]));//reqStr.format(lat, lon));
							infoWindow.open(map, marker);
					});
				}
			});
}

function submitRequest(bubble, lat, lon) {
	bubble.close();
}


function showRequest(location) {

	  iw = new google.maps.InfoWindow({
		content:	reqStr.format(location.lat(), location.lng()),
	    position: 	location,
	    map: map
	  });
	  $('#send_request').click(function(){
			submitRequest(iw, location.lat(), location.lng());
		});
	  
	  //markersArray.push(marker);
	}

function initialize() {
	var lajolla = new google.maps.LatLng(32.818062,-117.269440);
	var myOptions = {
	  center: lajolla,
	  zoom: 13,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
	google.maps.event.addListener(map, 'mousedown', function(event){ 
	    clearTimeout(map.pressButtonTimer); 
	    map.pressButtonTimer = setTimeout(function(){ 
	    	showRequest(event.latLng);
	    }, 800); 
	  }); 	
	google.maps.event.addListener(map, 'mouseup', function(event){ 
	    clearTimeout(map.pressButtonTimer); 
	  });
//	google.maps.event.addListener(map, 'click', function(event) {
//		showRequest(event.latLng);
//	});
	
	infoWindow	= new google.maps.InfoWindow();
	
	getMarkers();
	
}
