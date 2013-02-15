
// XXX: Fix default location: make a separate request

// Requires: main.js, modal.js

(function(){
    var map;
    var infoWindow;
    var markersArray    = [];
    var currMarker      = null;
    var currBubble      = null;
    var ilat        = 32.849885;   // La Jolla, CA
    var ilon        = -117.270298;
    var pressTimer;
    var defaultError    = "Service error. Please try again.";
    
    var dom = {
        inlineError:  function(msg) {
            return '<div class="alert alert-error" style="margin-top: 10px;">' + msg + '</div>';
        },
        fieldError:    function(msg) {
            return '<div class="alert alert-error error_spaces">' + msg + '</div>';
        }        
    };
    
    var ids = {
        show_reqs:  "#show_requests",
        remove_marker:  "#remove_marker"
    }

    //function(jqXHR, textStatus, errorThrown){
    //        // Structures error response
    //        var gen_error, errors;
    //        try {
    //            var data    = JSON.parse(jqXHR.responseText);
    //            errors      = data.errors;
    //            if ( data.error !== undefined) {
    //                gen_error = data.error;
    //            };
    //            // Display default general error only if errors are set
    //            if ($.isEmptyObject(errors) && gen_error === undefined) {
    //                gen_error = params.default_error;
    //            }
    //        } catch(err) {
    //            gen_error = params.default_error;
    //        }
    //        return {"errors": errors, "error": gen_error};
    //    }    

    
    var createMarker    = function(lat, lon, resource){
        // Creates marker and sets it on the map
        return new google.maps.Marker({
            position:  	new google.maps.LatLng(lat, lon),
            title:      resource,
            map:        map		// set map?
        });	
    }

    
    var showMarkers = function() {
        "Displays markers"
        $.ajax({
            url:    "/request/all/json",
            cache:  false,
            success:    function(data) {
                var reqs    = data.data;
                for (var i = 0; i < reqs.length; i++) {
                    var req	= reqs[i];
                    var marker	= createMarker(req_lat(req), req_lon(req), req.resource);
                    
                    onMarkerClick(marker, req)
                    markersArray.push(marker);
                }
            },
            error:  errorHandler
        });
    }
    
    var onMarkerClick   = function(marker, req){
        // Handles click event on marker
        //var lat	= req_lat(req);
        //var lon	= req_lon(req)
        google.maps.event.addListener(marker, 'click', function() {
            showInfo(marker, req.resource);
        });      
    }
    
    var submitRequest   = function(bubble, lat, lon){
        "Submits the request"
        $.ajax({
            url:    "/request/add",
            type:   "POST",
            cache:  false,
            data:   $("#request_form").serialize(),
            success:    function(data) {
                req = data.data;
                
                var marker  = createMarker(req_lat(req), req_lon(req), req.resource);
                markersArray.push(marker);
                
                onMarkerClick(marker, req);
                //// Set click event
                //google.maps.event.addListener(marker, 'click', function() {
                //    // Check if photo exists
                //    showInfo(marker, req.resource); // XXX: Finish
                //});
                bubble.close();
            },
            error: errorHandler(infoWindow)
        });
        
    }
    
    var _lat    = function(loc){
        return loc.lat().toFixed(6);
    }
    var _lon    = function (loc){
        return loc.lng().toFixed(6);
    }
    var req_lat = function(req){
        var lat	= req.lat/1e6;
        return lat.toFixed(6);
    }
    var req_lon = function(req){
        var lon	= req.lon/1e6;
        return lon.toFixed(6);
    }
    
    var openWindow  = function(iw, map, marker){
        if (currBubble) {
            currBubble.close();
        }
        iw.open(map, marker);
        currBubble  = iw;
        currMarker  = marker;
    }
    
    var errorData   = function(jqXHR, textStatus, errorThrown){
        // Structures error response
        var gen_error, errors;
        try {
            var data    = JSON.parse(jqXHR.responseText);
            errors      = data.errors;
            if ( data.error !== undefined) {
                gen_error = data.error;
            };
            // Display default general error only if errors are set
            if ($.isEmptyObject(errors) && gen_error === undefined) {
                gen_error = defaultError;
            }
        } catch(err) {
            gen_error = defaultError;
        }
        return {"errors": errors, "error": gen_error};
    }
   
    var errorHandler    = function(iw) {
        return function(jqXHR, textStatus, errorThrown){
            if (!iw){
                return;
            }
            var ed  = errorData(jqXHR, textStatus, errorThrown);
            if (ed.error) {
                iw.setContent(dom.inlineError(msg));
                iw.open(map);                
            }
            for (var k in ed.errors) {
                if (!ed.errors.hasOwnProperty(k)) {
                    continue;
                }
                $("#error_" + k).html(dom.fieldError(ed.errors[k]));
            }
            //google.maps.event.trigger(iw, 'content_changed');
            //iw.setContent(iw.getContent());
            //iw.open(map);
        }
    }
    
    // Bubbles
    var showRequest = function(location, req_data){
        // Displays request bubble
        if (infoWindow){
            // Close previous request bubble before opening a new one
            infoWindow.close(); 
        }
        infoWindow = new google.maps.InfoWindow({
            position:   location
        });
        $.ajax({
            url:    "/request/add?lat="+_lat(location)+"&lon="+_lon(location),
            cache:  false,
            success:    function(data){
                infoWindow.setContent(data.data);
                infoWindow.open(map);
                $('#send_request').click(function(e){
                    e.preventDefault();
                    submitRequest(infoWindow, _lat(location), _lon(location));
                });
            },
            error:  errorHandler(infoWindow)
        });
    }

    
    var onRemoveClick   = function(iw, marker, res){

        MODAL({
            container:  "modal_container",
            link:       "remove_request",
            url:        "/request/" + res + "/remove/json",
            header:     "Remove Request",
            btn_label:  "Remove Request",
            callback:   function(){
                iw.close();
                marker.setMap(null);
            }
        }).init();
        
        //$(ids.remove_marker).click(function(event) {
        //    $.get(base_api+"/" + id +"/remove", {"key": api_key}, // fix title
        //        function(data) {
        //            var res	= $.parseJSON(data);
        //            if (res["status"] == "ok") {
        //                iw.close();
        //                marker.setMap(null);
        //            }
        //        });
        //});        
    }
    
    var showInfo    = function(marker, resource) {
        // Makes request and shows window
        $.ajax({
            url:    "/request/info/" + resource,
            cache:  false,
            success:    function(data){
                var iw = new google.maps.InfoWindow({
                    content:   data.data
                });
                openWindow(iw, map, marker);
                
                onRemoveClick(iw, marker, resource)
            },
            error:  ""  // XXX: Fix
        });
    }

    
    var clearOverlays   = function() {
        if (markersArray) {
            for (var i = 0; i < markersArray.length; i++ ) {
                markersArray[i].setMap(null);
            }
        }
        markersArray  = [];
    }
    
    var onShowRequests  = function(chkBox, event){
        if (chkBox.is(":checked")){
            showMarkers();
        } else {
            clearOverlays();    
        }
    }    
    
    
    // Main function
    var initialize  = function(lat, lon){
        
        var location = new google.maps.LatLng(lat, lon);
        var myOptions = {
            center: location,
            zoom: 13,
            streetViewControl:  false,  // Enable if needed
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            draggableCursor: "crosshair"
        };
        map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);    // Create map
        
        // When drag starts, reset the timer
        google.maps.event.addListener(map, 'dragstart', function(){
            clearTimeout(pressTimer);
        });
        // Long click implementation (keep for now)
        google.maps.event.addListener(map, 'mousedown', function(event){
            clearTimeout(pressTimer);
            pressTimer = setTimeout(function(){ 
                
                map.setOptions({
                    draggable:  false
                });
                showRequest(event.latLng, null);               
            }, 500);
        }); 	
        google.maps.event.addListener(map, 'mouseup', function(event){
            map.setOptions({
                draggable:  true
            });                        
            clearTimeout(pressTimer); 
        });
    
        $(ids.show_reqs).change(function(e) {
            onShowRequests($(this), e);
        });
        onShowRequests($(ids.show_reqs));
    }    
    
    $(document).ready(function(){
	initialize(ilat, ilon);
    });    
})()