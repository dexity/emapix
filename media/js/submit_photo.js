

var PHOTOSUB = (function(options){
    "use strict"
    
    // modal_id:    #submit_modal
    // modal_body:  #submit_container
    // modal_error: #errors_container
    
    // Private variables
    var a,
    
    // Private functions
    init_fileupload = function(fopts) {
        // Required:
        var _fileupload  = fopts.fileupload || $('#fileupload');
        
        // Initialize the jQuery file upload widget
        _fileupload.fileupload({
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
    
        _fileupload.fileupload('option', {
            url:        options.select_url,
            maxFileSize: 5000000,
            minFileSize: 100,
            acceptFileTypes: /(\.|\/)(jpe?g|png)$/i,    // .jpg and .png images are allowed
            process: [
                {
                    action: 'load',
                    fileTypes: /^image\/(jpeg|png)$/,
                    maxFileSize: 10000000 // 20MB
                },
                {
                    action: 'resize',
                    maxWidth: 780,  // 920
                    maxHeight: 780
                },
                {
                    action: 'save'
                }
            ]
        });
    
    };
    
    
    // Public object
    var that = {
        // Functions
        show_select: function(){
            $.ajax({
                url:    options.select_url,
                type:   "GET",
                cache:  false,
                success:    function(data) {
                    $(".modal-backdrop").remove();
                    $("#submit_container").html(data);
                    $("#submit_modal").modal({backdrop: "static"});
                    
                    init_fileupload({});
                },
                error:  function(jqXHR, textStatus, errorThrown) {
                    $("#errors_container").html(format_error(jqXHR.responseText, errorThrown, true));
                    $("#submit_modal").modal({backdrop: "static"});
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
                    $("#submit_modal").modal({backdrop: "static"});
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    $("#submit_body").html(format_error(jqXHR.responseText, errorThrown));
                    $("#submit_modal").modal({backdrop: "static"});
                }
            });            
        },
        show_create: function(){
            
        }        
    }

    return that;
})