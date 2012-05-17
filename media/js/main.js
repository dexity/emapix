
var map;
var infoWindow;
var markersArray	= [];
var pressTimer;

//var base_api	= "http://localhost/api";
var base_api	= "http://ec2-184-73-88-189.compute-1.amazonaws.com/api";
var base_s3		= "https://s3.amazonaws.com/emapix_uploads";
var api_key		= "0dae2799bb2d9b88e1d38a337377b221";

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
	
var actionStr	= '<img id="img_id" src="#" alt="" width=200 hidden=true/></br>' + 
	'Location: {0}; {1}<br/>' +
	'<input type="file" name="uploaded" />' +
	'<button type="button" id="upload_picture">Upload Picture</button><br/>' +
	'<button type="button" id="remove_marker">Remove Marker</button><br/>';
		
var viewStr		= '<img src="{0}" width=200/><br/>' +
'<button type="button" id="remove_marker">Remove</button>';

function createMarker(lat, lon, resource) {
	// Creates marker and sets it on the map
	return new google.maps.Marker({
	    position:  	new google.maps.LatLng(lat, lon),
	    title:		resource,
	    map:		map		// set map?
	    });	
}

function imageUri(resource) {
	return "{0}/{1}.jpg".format(base_s3, resource);
}

function showMarkers() {
	$.get(base_api + "/all", {"key": api_key},
			function(data) { 
				var res	= $.parseJSON(data);
				var reqs	= res["result"];
				for (i in reqs) {
					req	= reqs[i];
					marker	= createMarker(req_lat(req), req_lon(req), req["resource"]);
					// Add click listener in closure
					(function(){
						var _marker = marker;
						var _req	= req;
						var lat		= req_lat(_req);
						var lon		= req_lon(_req)
						// Refactor?
						google.maps.event.addListener(_marker, 'click', function() {
							uri	= imageUri(_marker.title);
							// Check if photo exists
							if (_req["photo_exists"]) {
								showView(_marker, uri, _req["id"]);
							} else {
								showAction(_marker, lat, lon, _req["id"]);
							}
						});		
					})();
					markersArray.push(marker);
				}
			});
}

function randomStr() {
	// Returns 16 characters string
	var chars = "0123456789abcdef";
	var string_length = 32;
	var randomstring = '';
	for (var i=0; i<string_length; i++) {
		var rnum = Math.floor(Math.random() * chars.length);
		randomstring += chars.substring(rnum,rnum+1);
	}
	return randomstring;
}

function submitRequest(bubble, lat, lon) {
	$.get(base_api+"/add", {"key": api_key, "lat": Math.round(lat*1e6), 
							"lon": Math.round(lon*1e6), "resource": randomStr()}, 
			function(data){
				var res	= $.parseJSON(data);
				if (res["status"] == "ok") {
					req	= res["result"]
					var marker	= createMarker(req_lat(req), req_lon(req), req["resource"]);
				}
				// display error
				google.maps.event.addListener(marker, 'click', function() {
					// Check if photo exists
					showAction(marker, req_lat(req), req_lon(req), req["id"]);
				});								
				
			});
	bubble.close();
}

function _lat(loc) { return loc.lat().toFixed(6); }
function _lon(loc) { return loc.lng().toFixed(6); }
function req_lat(req) {
	lat	= req["lat"]/1e6;
	return lat.toFixed(6);
}
function req_lon(req) {
	lon	= req["lon"]/1e6;
	return lon.toFixed(6);
}

// Bubbles
function showRequest(location) {

	  iw = new google.maps.InfoWindow({
		content:	reqStr.format(_lat(location), _lon(location)),
	    position: 	location,
	    map: map
	  });
	  $('#send_request').click(function(){
			submitRequest(iw, _lat(location), _lon(location));
		});
	}

function showView(marker, uri, id) {
	iw = new google.maps.InfoWindow({
		content:	viewStr.format(uri),
	});	
	iw.open(map, marker);
	
	// Refactor?
	$('button#remove_marker').click(function(event) {
		$.get(base_api+"/" + id +"/remove", {"key": api_key}, // fix title
				function(data) {
					var res	= $.parseJSON(data);
					if (res["status"] == "ok") {
						iw.close();
						marker.setMap(null);
					}
				});
	});
}

function showAction(marker, lat, lon, id) {
	iw = new google.maps.InfoWindow({
		content:	actionStr.format(lat, lon, api_key, marker.title),
	});
	iw.open(map, marker);
	
	$('input').change(function(){
		// Set image
	    if (this.files && this.files[0]) {
	        var reader = new FileReader();
	        reader.onload = function (e) {
	        	$('#img_id').show();
	            $('#img_id').attr('src', e.target.result);
	        }
	        reader.readAsDataURL(this.files[0]);
	    }
	});
	
	$('button#upload_picture').click(function(event) {
		var data = new FormData();
		$.each($('input')[0].files, function(i, file) {
		    data.append('uploaded', file);	// should have one file
		});
		$.ajax({
		    url: 	base_api + "/upload?key=" + api_key + "&resource=" + marker.title,
		    data: 	data,
		    cache: 	false,
		    contentType: false,
		    processData: false,
		    type: 	'POST',
		    success: function(data){
				
				google.maps.event.clearListeners(marker, "click");	// Remove listeners
						    	
		    	// Refactor?
				google.maps.event.addListener(marker, 'click', function() {
					uri	= imageUri(marker.title);
					showView(marker, uri, id);
				});								
		    	
		    	iw.close();
		    }
		});
		
	});
	
	// Refactor?
	$('button#remove_marker').click(function(event) {
		$.get(base_api+"/" + id +"/remove", {"key": api_key}, // fix title
				function(data) {
					var res	= $.parseJSON(data);
					if (res["status"] == "ok") {
						iw.close();
						marker.setMap(null);
					}
				});
	});
}


// Main function
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
	
	infoWindow	= new google.maps.InfoWindow();
	
	showMarkers();
	
}
