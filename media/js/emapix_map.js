
// XXX: Fix default location: make a separate request

// Requires main.js 

(function(){
    var map;
    var infoWindow;
    var markersArray    = [];
    var currMarker      = null;
    var currBubble      = null;
    var ilat     = 32.849885;   // La Jolla, CA
    var ilon     = -117.270298;
    var pressTimer;
    var defaultError    = "Service error. Please try again.";
    
    var base_api	= "http://localhost/api";
    var host        = "http://localhost";
    //var base_api	= "http://ec2-184-73-88-189.compute-1.amazonaws.com/api";
    var base_s3		= "https://s3.amazonaws.com/emapix_uploads";
    var api_key		= "0dae2799bb2d9b88e1d38a337377b221";
    
    var dom = {
        inline_error:  function(msg) {
            return '<div class="alert alert-error" style="margin-top: 10px;">' + msg + '</div>';
        }
    }
    String.prototype.format = function() {
            var args = arguments;
            return this.replace(/{(\d+)}/g, function(match, number) { 
              return typeof args[number] != 'undefined'
                ? args[number]
                : match
              ;
            });
        };

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

    var infoStr  = '<div style="margin-bottom: 10px;"><i>{0}</i></div>' + 
        '<b>Location</b>: {1}; {2}' +
        '<div style="margin-top: 10px;"><a href="#" target="_blank" class="pull-left">Request Details</a>' +
        '<a href="" target="_blank" class="pull-right" style="color: red;">Remove</a><div>';
        
    //var actionStr	= '<img id="img_id" src="#" alt="" width=200 hidden=true/></br>' + 
    //    'Location: {0}; {1}<br/>' +
    //    '<input type="file" name="uploaded" />' +
    //    '<button type="button" id="upload_picture">Upload Picture</button><br/>' +
    //    '<button type="button" id="remove_marker">Remove Marker</button><br/>';
    
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
        $.get(host + "/request/all/json",
            function(data) { 
                var res	= $.parseJSON(data);
                if (res["status"] == "fail")
                    return;
                
                var reqs	= res["result"];
                for (i in reqs) {
                    var req	= reqs[i];
                    var marker	= createMarker(req_lat(req), req_lon(req), req["resource"]);
                    
                    // Add click listener in closure
                    (function(){
                        var _marker = marker;
                        var _req	= req;
                        var lat	= req_lat(_req);
                        var lon	= req_lon(_req)
                        google.maps.event.addListener(_marker, 'click', function() {
                            // Will not make a separate request for every marker
                            showInfo(_marker, _req["resource"]);
                            
                            /*uri	= imageUri(_marker.title);
                            showAction(_marker, lat, lon, _req["id"]);
                            
                            // Check if photo exists
                            if (_req["photo_exists"]) {
                                showView(_marker, uri, _req["id"]);
                            } else {
                                showAction(_marker, lat, lon, _req["id"]);
                            }
                            */
                        });		
                    })();
                    markersArray.push(marker);
                }
            });
    }
    
    
    function submitRequest(bubble, lat, lon)
    {
        $.post(host+"/request/add",
            $("#request_form").serialize(),
            function(data){
                try
                {
                    var res	= $.parseJSON(data);
                    if ("status" in res && res["status"] == "ok") {
                        var req	= res["result"]
                        var marker	= createMarker(req_lat(req), req_lon(req), req["resource"]);
                        markersArray.push(marker);
                        
                        // Set click event
                        google.maps.event.addListener(marker, 'click', function() {
                            // Check if photo exists
                            showInfo(marker, req["resource"]);
                        });
                        bubble.close();
                    }
                }
                catch (e){
                    // Not json
                    infoWindow.setContent(data);
                }
            });
        
    }
    
    function _lat(loc) { return loc.lat().toFixed(6); }
    function _lon(loc) { return loc.lng().toFixed(6); }
    function req_lat(req) {
            var lat	= req["lat"]/1e6;
            return lat.toFixed(6);
    }
    function req_lon(req) {
            var lon	= req["lon"]/1e6;
            return lon.toFixed(6);
    }
    // Keep it for now
    function wrap_content(content, id)
    {
        return '<div id="'+id+'">'+content+'</div>';
    }
    
    function openWindow(iw, map, marker)
    {
        if (currBubble) {
            currBubble.close();
        }
        iw.open(map, marker);
        currBubble  = iw;
        currMarker  = marker;
    }
    
    var errorHandler    = function(iw) {
        return function(jqXHR, textStatus, errorThrown){
            if (!iw){
                return;
            }
            var msg = defaultError;
            try {
                var error  = JSON.parse(jqXHR.responseText).error;
                if ( error !== undefined) {
                    msg = error;
                };
            } catch(err) {}
            iw.setContent(dom.inline_error(msg));
            iw.open(map);
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
            success:    function(data){
                iw.setContent(s);
                iw.open(map);
                $('#send_request').click(function(e){
                    e.preventDefault();
                    submitRequest(infoWindow, _lat(location), _lon(location));
                });
            },
            error:  errorHandler(infoWindow)
        });
    }

    
    function showView(marker, uri, id) {
        var iw = new google.maps.InfoWindow({
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
    
    function showInfo(marker, resource) {
        $.get("/request/info/" + resource,
            function(data){
              var iw = new google.maps.InfoWindow({content:   data});            
              openWindow(iw, map, marker);
            });
    }
    
    // XXX: Refactor
    function showAction(marker, lat, lon, id) {
        var iw = new google.maps.InfoWindow({
            content:    actionStr.format(lat, lon, api_key, marker.title),
        });
        iw.open(map, marker);
        
        /*
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
        */
    }
    
    function clearOverlays() {
      if (markersArray) {
        for (var i = 0; i < markersArray.length; i++ ) {
          markersArray[i].setMap(null);
        }
      }
      markersArray  = [];
    }
    
    function onShowRequests(chkBox, event)
    {
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
    
        //$("#show_requests").change(function(e) {
        //    onShowRequests($(this), e);
        //});
        //onShowRequests($("#show_requests"));
    
        //// Remove request
        //$(document).on("click", "#remove_link", function(e){
        //    e.preventDefault();
        //    $("#body_errors").html("");
        //    $("#remove_modal").modal();
        //});
    }    
    
    $(document).ready(function(){
	initialize(ilat, ilon);
    });    
})()