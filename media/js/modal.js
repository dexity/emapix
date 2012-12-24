

// Form handler for modals

var MODAL = (function(options){
    "use strict"
    
    var params = {
        container:  "#" + options.container,
        link:       "#" + options.link,
        modal:      "#modal",
        modal_status:   "#modal_status",
        body:       options.body,
        url:        options.url,
        header:     options.header,
        extra_fields:   options.extra_fields,
        callback:   options.callback,
        btn_label:  (options.btn_label ? options.btn_label : "Save Changes"),
        error_base:     "#error_",
        default_error:  "Service error. Please try again."
    },
    dom = {
        modal:  function(header) {
            var s   = '<div id="modal" class="modal hide fade">' +
                '   <div class="modal-header">' +
                '       <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>' +
                '       <h3>' + params.header + '</h3>' +
                '   </div>' +
                '   <div class="modal-body"></div>' +
                '   <div class="modal-footer">' +
                '       <div id="modal_status"></div>' +
                '       <button class="btn btn-primary submit_form">' + params.btn_label + '</button>' +
                '       <a href="#" data-dismiss="modal">Cancel</a>' +
                '   </div>'+
                '</div>';
                
            return s;
        },
        inline_error:  function(msg) {
            return '<div class="e-alert e-alert-inline alert-error pull-left">' + msg + '</div>';
        },
        field_error:    function(msg) {
            return '<div class="alert alert-error error_spaces">' + msg + '</div>';
        },
        spinner:    '<img src="/media/img/spinner_small.gif" class="e-button-spinner"/>'
    };
    
    // Public object
    var that = {
        init:   function(){
            $(params.link).click(function(e) {
                e.preventDefault();
                $(params.container).html(dom.modal());
                if (params.body !== undefined){
                    // Set modal body if it is set
                    that.set_modal(params.body);
                } else {
                    // Load modal body
                    $.ajax({
                        url:        params.url,
                        type:       "GET",
                        cache:      false,
                        success:    function(data){
                            that.set_modal(data.data);
                        },
                        error:  that.error_modal
                    });
                }
            });
        },
        set_modal:  function(content){
            $(params.modal + " .modal-body").html(content);
            $(params.modal).modal();
            $(params.modal + " .submit_form").unbind().click(that.submit_form);            
        },
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
            $(params.modal).modal();            
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
        submit_form:    function(){
            
            var fields  = $(params.modal + " form").serialize() || {};
            console.debug(fields);
            if (typeof params.extra_fields === "object"){
                for (var key in params.extra_fields){
                    if (params.extra_fields.hasOwnProperty(key)){
                        fields[key] = params.extra_fields[key]; // Update fields
                    }
                }
            }
            // Submits form
            var ajaxopts    = {
                url:        params.url,
                type:       "POST",
                data:       fields,
                cache:      false,
                beforeSend: function(){
                    that.init_process();
                },
                success:    function(data){
                    that.end_process();
                    if (typeof params.callback == "function"){
                        params.callback();
                    }
                },
                error:  that.error_modal
            }
            $.ajax(ajaxopts);    
        }      
    }
    
    return that;
})