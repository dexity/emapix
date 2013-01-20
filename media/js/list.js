
// Requires:
//      mustache.js
//      paginator.js

var LIST    = (function(options){
    "use strict"
    
    var params = {
        $container:     options.container,
        templates:      options.templates,
        dataProp:       options.dataProp,
        itemProps:      options.itemProps,  // Maps data to template params
        $spinner:       options.spinner,
        baseUrl:        options.baseUrl,
        defaultError:   "Service error. Please try again.",
        fnItemCreated:  options.fnItemCreated,
        paginator:      PAGES({})
    };
    
    var utils   = {
        compTmpl:      function($tmpl){
            // Compiles template with mustache
            return Mustache.compile($tmpl.html());
        }
    },
    dom = {
        item:           utils.compTmpl(params.templates.item),
        spinner:        utils.compTmpl(params.templates.spinner),
        error:          utils.compTmpl(params.templates.error)
    };
    

    // Public object
    var that = {
        initProcess:   function(){
            $(".alert-error").hide();   // Hide errors
        },
        stopProcess:   function(){
            $(params.$spinner).empty();
        },        
        loadError:   function(jqXHR, textStatus, errorThrown) {
            // Error when comments are loaded
            var msg = that.error_msg(jqXHR, textStatus, errorThrown);
            $(params.container).html(dom.error({"error": msg}));
        },
        error_msg:  function(jqXHR, textStatus, errorThrown) {
            that.stopProcess();
            var msg = params.defaultError;
            try {
                var js  = JSON.parse(jqXHR.responseText);
                if ( js.error !== undefined) {
                    msg = error;
                } else if (typeof js.errors === "object") {
                    var keys    = Object.keys(js.errors);
                    if (keys.length > 0){
                        msg = js.errors[keys[0]];
                    }
                };
            } catch(err) {}
            return msg;
        },
        load:  function(url){
            $.ajax({
                url:        (url !== undefined) ? url : params.baseUrl,
                type:       "GET",
                cache:      false,
                beforeSend: function() {
                    $(params.$spinner).html(dom.spinner());
                },
                success:    function(data) {
                    $(params.$container).empty();
                    that.stopProcess();
                    
                    var items    = data.data[params.dataProp];
                    if ( items === undefined){
                        return;     // No items available
                    }
                    // Create paginator and set it in container
                    for (var i = 0; i < items.length; i++){
                        var item = items[i],
                            d   = {};
                        for (var key in params.itemProps){
                            if (params.itemProps.hasOwnProperty(key)){
                                d[key]  = item[params.itemProps[key]];
                            }
                        }
                        var o   = $(dom.item(d));
                        $(params.$container).append(o);
                        if (typeof params.fnItemCreated === "function"){
                            params.fnItemCreated(o);
                        }
                    }
                    if (data.data.paging !== undefined && params.paginator !== undefined){
                        $(params.$container).append(params.paginator.show_pages(params.baseUrl,
                                                           data.data.paging.page,
                                                           data.data.paging.total));
                    }
                    //if (params.submit_base_url !== undefined){
                    //    $(params.container).append(dom.submit_form({}));
                    //}
                    //
                    // Register click events for pages
                    $(".pagination li").click(function(e){
                        e.preventDefault();
                        var aa   = $(this).find("a");
                        if (!(aa.length > 0 && $(aa[0]).attr("href"))) {
                            return;
                        }
                        that.load($(aa[0]).attr("href"));
                    });
                    //// Register click event for comment submission
                    //if (params.submit_id) {
                    //    $(params.submit_id).unbind()
                    //        .click(that.submit_form);
                    //}
                },
                error:  that.loadError
            });
        }
    }
    
    return that;
})    
    