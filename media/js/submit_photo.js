
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
    params = {
        modal_container:  utils.select_option("modal_container", "submit_container"),
        modal:            utils.select_option("modal", "submit_modal"),
        modal_body:       utils.select_option("modal_body", "submit_body"),
        fileupload:       utils.select_option("fileupload", "fileupload"),
        cropper_form:     utils.select_option("cropper_form", "cropper_form"),
        create_form:      utils.select_option("create_form", "create_form"),
        modal_status:     "#modal_status",
        error_base:       "#error_",
        default_error:    "Service error. Please try again.",
        max_size:         options.max_size || 400
    },
    // Private functions    
    init_fileupload = function() {
        
        // Initialize the jQuery file upload widget
        $(params.fileupload).fileupload({
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
        .bind("fileuploadsend", function(e, data) {
            $(".alert-error").hide();
        })
        .bind("fileuploaddone", function(e, data) {
            if (data.result[0].success) {
                that.show_crop();
            }
        })
    
        $(params.fileupload).fileupload('option', {
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
                    action:     'resize',
                    maxWidth:   params.max_size,
                    maxHeight:  params.max_size
                },
                {
                    action: 'save'
                }]
        });
    
    },
    init_cropper    = function(){
        
        var jcrop_api = {
            size:           options.crop_size,
            submit_crop:    function(){
                $.ajax({
                    url:    options.crop_url,
                    type:   "POST",
                    data:   $(params.cropper_form).serialize(),
                    cache:  false,
                    beforeSend: function(){
                        that.init_process();
                    },
                    success:    function(data) {
                        that.show_create();
                    },
                    error:  that.error_modal
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
            $.ajax({
                url:    options.create_url,
                type:   "POST",
                data:   $(params.create_form).serialize(),
                cache:  false,
                beforeSend: function(){
                    that.init_process();
                },
                success:    function(data) {
                    $(params.modal).modal("hide");
                    if (typeof options.finished_callback === "function"){
                        options.finished_callback();
                    }
                },
                error:  that.error_modal
            });
        })        
    },
    dom = {
        inline_error:  function(msg) {
            return '<div class="alert alert-error e-alert-inline pull-left">' + msg + '</div>';
        },
        field_error:    function(msg) {
            return '<div class="alert alert-error error_spaces">' + msg + '</div>';
        },
        spinner:    '<img src="/media/img/spinner_small.gif" class="e-button-spinner"/>'        
    };
    
    
    // Public object
    var that = {
        // Properties
        error_data:     function(jqXHR, textStatus, errorThrown){
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
                    gen_error = params.default_error;
                }
            } catch(err) {
                gen_error = params.default_error;
            }
            return {"errors": errors, "error": gen_error};
        },
        error_modal:    function(jqXHR, textStatus, errorThrown){
            that.end_process();
            var ed  = that.error_data(jqXHR, textStatus, errorThrown);
            if (ed.error) {
                $(params.modal_status).html(dom.inline_error(ed.error));
            }
            for (var k in ed.errors) {
                if (!ed.errors.hasOwnProperty(k)) {
                    continue;
                }
                $(params.error_base + k).html(dom.field_error(ed.errors[k]));
            }
            // Enable button
            $(params.modal).modal({backdrop: "static"});            
        },
        init_process:   function(){
            $(".alert-error").hide();   // Hide errors
            $(params.modal_status).html(dom.spinner);     // Show spinner
            $(".modal-footer button").attr({"disabled": "disabled"})    // Disable button
                .removeClass("disabled").addClass("disabled");               
        },
        end_process:    function(){
            $(params.modal_status).empty();
            $(".modal-footer button").removeClass("disabled").removeAttr("disabled");
        },
        init_success:   function(data){
            $(".modal-backdrop").remove();
            $(params.modal_container).html(data);
            $(params.modal).modal({backdrop: "static"});
        },
        // Functions
        show_select: function(){
            $.ajax({
                url:    options.select_url,
                type:   "GET",
                cache:  false,
                success:    function(data) {
                    that.init_success(data);
                    init_fileupload();
                },
                error:  that.error_modal
            });        
        },
        show_crop: function(){
            // Load crop image modal page (doesn't handle image crop)
            $.ajax({
                url:    options.crop_url,
                type:   "GET",
                cache:  false,
                success: function(data) {
                    that.init_success(data);
                    init_cropper();
                },
                error:  that.error_modal
            });
        },
        show_create: function(){
            // Loads create image modal page (doesn't handle images creation)
            $.ajax({
                url:    options.create_url,
                type:   "GET",
                cache:  false,
                success: function(data) {
                    that.init_success(data);
                    init_create();
                },
                error: that.error_modal
            });
        }        
    }

    return that;
})