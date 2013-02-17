
// XXX: Fix default location: make a separate request

// Requires: main.js, modal.js

(function(){
    var map;
    var reqWindow;
    var markersArray    = [];
    var currMarker;
    var currWindow;
    var ilat            = 32.849885;   // La Jolla, CA
    var ilon            = -117.270298;
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
        show_reqs:      "#show_requests",
        remove_marker:  "#remove_marker",
        request_form:   "#request_form",
        send_request:   "#send_request"
    }

    var createMarker    = function(lat, lon, resource){
        // Creates marker and sets it on the map
        return new google.maps.Marker({
            position:  	new google.maps.LatLng(lat, lon),
            title:      resource,
            map:        map		// Set map
        });	
    }

    
    var showMarkers = function() {
        // Displays markers
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
            }
            //error:  errorHandler
        });
    }
    
    var onMarkerClick   = function(marker, req){
        // Handles click event on marker
        google.maps.event.addListener(marker, 'click', function() {
            showInfo(marker, req.resource);
        });      
    }
    
    var submitRequest   = function(iw, lat, lon){
        // Submits the request
        
        $.ajax({
            url:    "/request/add",
            type:   "POST",
            cache:  false,
            data:   $(ids.request_form).serialize(),
            success:    function(data) {
                req = data.data;
                
                var marker  = createMarker(req_lat(req), req_lon(req), req.resource);
                currMarker  = marker;
                
                onMarkerClick(marker, req);
                markersArray.push(marker);
                iw.close();
            },
            error: errorHandler(iw)
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
        // Opens window for marker
        if (currWindow) {
            currWindow.close();
        }
        iw.open(map, marker);
        currWindow  = iw;
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
   
    var errorHandler    = function(iw, marker) {
        // Handles errors
        return function(jqXHR, textStatus, errorThrown){
            if (!iw){
                return;
            }
            var ed  = errorData(jqXHR, textStatus, errorThrown);
            if (ed.error) {
                iw.setContent(dom.inlineError(ed.error));
                iw.open(map, marker);                
            }
            for (var k in ed.errors) {
                if (!ed.errors.hasOwnProperty(k)) {
                    continue;
                }
                $("#error_" + k).html(dom.fieldError(ed.errors[k]));
            }
        }
    }
    
    // Entry function for sending request
    var showRequest = function(location){
        // Displays request window
        if (reqWindow){
            // Close previous request window before opening a new one
            reqWindow.close(); 
        }
        reqWindow = new google.maps.InfoWindow({
            position:   location
        });
        $.ajax({
            url:    "/request/add?lat="+_lat(location)+"&lon="+_lon(location),
            cache:  false,
            success:    function(data){
                reqWindow.setContent(data.data);
                reqWindow.open(map);
                $(ids.send_request).click(function(e){
                    e.preventDefault();
                    submitRequest(reqWindow, _lat(location), _lon(location));
                });
            },
            error:  errorHandler(reqWindow)
        });
    }

    
    var onRemoveClick   = function(iw, marker, res){
        // Handles remove request click
        google.maps.event.addListener(iw, 'domready', function(event){
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
        });
    }
    
    var showInfo    = function(marker, resource) {
        // Makes request and shows window
        var iw = new google.maps.InfoWindow();        
        $.ajax({
            url:    "/request/info/" + resource,
            cache:  false,
            success:    function(data){
                iw.setContent(data.data);
                openWindow(iw, map, marker);
                
                onRemoveClick(iw, marker, resource)
            },
            error:  errorHandler(iw, marker)
        });
    }
    
    var clearOverlays   = function() {
        // Clears markers from the map
        if (markersArray) {
            for (var i = 0; i < markersArray.length; i++ ) {
                markersArray[i].setMap(null);
            }
        }
        markersArray  = [];
    }
    
    var onShowRequests  = function(chkBox, event){
        // Handles check event to display all requests
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
            streetViewControl:  true,  // Enable if needed
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
                showRequest(event.latLng);               
            }, 500);
            event.stop();
        }); 	
        google.maps.event.addListener(map, 'mouseup', function(event){
            map.setOptions({
                draggable:  true
            });                        
            clearTimeout(pressTimer); 
            event.stop();
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