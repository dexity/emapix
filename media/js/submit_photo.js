
// XXX: Disable button when in progress

var PHOTOSUB = (function(options){
    "use strict"
    
    // Private objects
    var utils = {
        conv2selector: function(sel) {
            // Appends # to sel string
            if (typeof sel === "string") {
                return "#"+sel;
            }
            return null;
        },
        select_option: function(sel, def) {
            return this.conv2selector(options[sel] || def);
        }
    },
    modal           = utils.select_option("modal", "submit_modal"),
    modal_body      = utils.select_option("modal_body", "submit_body"), //"submit_container",
    modal_error     = utils.select_option("modal_error", "errors_container"),
    modal_progress  = utils.select_option("modal_progress", "progress"),
    fileupload      = utils.select_option("fileupload", "fileupload"),
    cropper_form    = utils.select_option("cropper_form", "cropper_form"),
    create_form     = utils.select_option("create_form", "create_form"),

    // Private functions    
    init_fileupload = function() {
        
        // Initialize the jQuery file upload widget
        $(fileupload).fileupload({
            autoUpload:         true,
            uploadTemplateId:   "template-content",
            downloadTemplateId: "template-content",
            filesContainer:     $("#files_container"),
            add:                function(e, data) {
                
                var that    = $(this).data('fileupload'),
                    options = that.options,
                    files   = data.files;
                $(this).fileupload('process', data).done(function () {
                    that._adjustMaxNumberOfFiles(-files.length);
                    data.maxNumberOfFilesAdjusted = true;
                    data.files.valid = data.isValidated = that._validate(files);
                    data.context = that._renderUpload(files).data('data', data);
                    
                    options.filesContainer.html(data.context);  // Replace files container
    
                    that._renderPreviews(files, data.context);
                    that._forceReflow(data.context);
                    that._transition(data.context).done(
                        function () {
                            if ((that._trigger('added', e, data) !== false) &&
                                    (options.autoUpload || data.autoUpload) &&
                                    data.autoUpload !== false && data.isValidated) {
                                data.submit();
                            }
                        }
                    );
                });
            }
        })
        .bind("fileuploaddone", function(e, data) {
            
            if (data.result[0].success) {
                that.show_crop();    // From request.html
            }
        })
    
        $(fileupload).fileupload('option', {
            url:        options.select_url,
            maxFileSize: 5000000,
            minFileSize: 100,
            acceptFileTypes: /(\.|\/)(jpe?g|png)$/i,    // .jpg and .png images are allowed
            process: [{
                    action: 'load',
                    fileTypes: /^image\/(jpeg|png)$/,
                    maxFileSize: 10000000 // 20MB
                },
                {
                    action: 'resize',
                    maxWidth: 780,
                    maxHeight: 780
                },
                {
                    action: 'save'
                }]
        });
    
    },
    init_cropper    = function(){
        
        var jcrop_api = {
            size:   options.crop_size,
            submit_crop:    function(){
                $(modal_progress).show();
                $.ajax({
                    url:    options.crop_url,
                    type:   "POST",
                    data:   $(cropper_form).serialize(),
                    cache:  false,
                    success:    function(data) {
                        that.show_create();  // From request.html
                    },
                    error:  function(jqXHR, textStatus, errorThrown) {
                        $(modal_progress).hide();
                        
                        var msg = '<div class="e-alert e-alert-inline alert-error">';
                        msg += format_error(jqXHR.responseText, errorThrown, true);
                        msg += '</div>';
                        $(modal_error).html(msg);
                    }
                });
            },
            updateCoords:   function(c){
                $('input[name=x]').val(c.x);
                $('input[name=y]').val(c.y);
                $('input[name=w]').val(c.w);
                $('input[name=h]').val(c.h);
            },
            getAspectRatio: function(bounds) {
                return bounds[0] > this.size && bounds[1] > this.size ? 1 : undefined;
            },
            getSelect:  function(bounds) {
                var x2 = bounds[0] > this.size ? this.size : bounds[0],
                    y2 = bounds[1] > this.size ? this.size : bounds[1];
                return [0, 0, x2, y2];
            },
            getMinSize: function(bounds) {
                var w = bounds[0] > this.size ? this.size : bounds[0],
                    h = bounds[1] > this.size ? this.size : bounds[1];
                return [w, h];
            },
            getMaxSize: function(bounds) {
                var aspect  = this.getAspectRatio(bounds);
                if (aspect == 1) {
                    var w = bounds[0] > this.size ? bounds[0] : this.size,
                        h = bounds[1] > this.size ? bounds[1] : this.size;
                    return [w, h];
                } else {
                    return this.getMinSize(bounds);
                }
            },
            set_cropper:    function() {
                var jcrop   = $.Jcrop('#cropbox');
                var bounds  = jcrop.getBounds();
                jcrop.setOptions({
                    aspectRatio: this.getAspectRatio(bounds),
                    setSelect:  this.getSelect(bounds),
                    minSize:    this.getMinSize(bounds),
                    maxSize:    this.getMaxSize(bounds),
                    onSelect:   this.updateCoords
                });
            }
        };
        
        $("#cropbox").load(function(){
            jcrop_api.set_cropper();
        });
        
        $("#crop_image").click(function(){
            jcrop_api.submit_crop();
        });
        $("#select_file").click(function(e){
            e.preventDefault();
            that.show_select();
        });    
    },
    init_create     = function(){
        $("#select_file").click(function(e){
            e.preventDefault();
            that.show_select();
        });
        
        $("#submit_image").click(function(){
            $(modal_progress).show();
            $.ajax({
                url:    options.create_url,
                type:   "POST",
                data:   $(create_form).serialize(),
                cache:  false,
                success:    function(data) {
                    options.finished_callback();
                },
                error:  function(jqXHR, textStatus, errorThrown) {
                    $(modal_progress).hide();
                    
                    var msg = '<div class="e-alert e-alert-inline alert-error">';
                    msg += format_error(jqXHR.responseText, errorThrown, true);
                    msg += '</div>';
                    $(modal_error).html(msg);
                }
            });
        })        
    };
    
    
    // Public object
    var that = {
        // Properties
        
        // Functions
        show_select: function(){
            $.ajax({
                url:    options.select_url,
                type:   "GET",
                cache:  false,
                success:    function(data) {
                    $(".modal-backdrop").remove();
                    $("#submit_container").html(data);
                    $(modal).modal({backdrop: "static"});
                    
                    init_fileupload({});
                },
                error:  function(jqXHR, textStatus, errorThrown) {
                    $(modal_error).html(format_error(jqXHR.responseText, errorThrown, true));
                    $(modal).modal({backdrop: "static"});
                }
            });        
        },
        show_crop: function(){
            // Load crop image modal page (doesn't handle image crop)
            $.ajax({
                url:    options.crop_url,
                type:   "GET",
                cache:  false,
                success: function(data) {
                    $(".modal-backdrop").remove();
                    $("#submit_container").html(data);
                    $(modal).modal({backdrop: "static"});
                    
                    init_cropper();
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    $(modal_body).html(format_error(jqXHR.responseText, errorThrown));
                    $(modal).modal({backdrop: "static"});
                }
            });
        },
        show_create: function(){
            // Loads create image modal page (doesn't handle images creation)
            $.ajax({
                url:    options.create_url,
                type:   "GET",
                cache:  false,
                success: function(data) {
                    $(".modal-backdrop").remove();
                    $("#submit_container").html(data);
                    $(modal).modal({backdrop: "static"});
                    
                    init_create();
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    $(modal_body).html(format_error(jqXHR.responseText, errorThrown));
                    $(modal).modal({backdrop: "static"});
                }
            });
        }        
    }

    return that;
})