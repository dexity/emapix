
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
        //fnItemCreated:  options.fnItemCreated,
        //fnInitComplete: options.fnInitComplete,
        paginator:      PAGES({})
    };
    
    var aux   = {
        compTmpl:   function($tmpl){
            // Compiles template with mustache
            return Mustache.compile($tmpl.html());
        },        
        getData:    function(o, path){
            // Tries to traverse the object by path
            try {
                var parts   = path.split(".");
                var val     = o[parts[0]];
                for (var i = 1; i < parts.length; i++){
                    val = val[parts[i]];
                }
                return val;
            } catch(err){}
            return null;
        }
    };
    

    // Public object
    var that = {
        utils:  {
            compTmpl:   aux.compTmpl,
        },
        dom:    {
            item:           aux.compTmpl(params.templates.item),
            spinner:        aux.compTmpl(params.templates.spinner),
            error:          aux.compTmpl(params.templates.error)
        },
        getParams:  function(){
            return params;
        },
        initProcess:   function(){
            $(".alert-error").hide();   // Hide errors
        },
        stopProcess:   function(){
            params.$spinner.empty();
        },
        loadError:   function(jqXHR, textStatus, errorThrown) {
            // Error when comments are loaded
            var msg = that.errorMsg(jqXHR, textStatus, errorThrown);
            params.$container.html(that.dom.error({"error": msg}));
        },
        errorMsg:  function(jqXHR, textStatus, errorThrown) {
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
                    params.$spinner.html(that.dom.spinner());
                },
                success:    function(data) {
                    params.$container.empty();
                    that.stopProcess();
                    
                    var items    = aux.getData(data, params.dataProp);
                    if ( items === undefined){
                        return;     // No items available
                    }
                    // Create paginator and set it in container
                    for (var i = 0; i < items.length; i++){
                        var item = items[i],
                            d   = {};
                        for (var key in params.itemProps){
                            if (params.itemProps.hasOwnProperty(key)){
                                d[key]  = aux.getData(item, params.itemProps[key]);
                            }
                        }
                        var o   = $(that.dom.item(d));
                        params.$container.append(o);
                        if (typeof options.fnItemCreated === "function"){
                            options.fnItemCreated(o);
                        }
                    }
                    if (data.data.paging !== undefined && params.paginator !== undefined){
                        params.$container.append('<div style="clear: both"></div>');
                        params.$container.append(params.paginator.show_pages(params.baseUrl,
                                                           data.data.paging.page,
                                                           data.data.paging.total));
                    }
                    // Register click events for pages
                    $(".pagination li").click(function(e){
                        e.preventDefault();
                        var aa   = $(this).find("a");
                        if (!(aa.length > 0 && $(aa[0]).attr("href"))) {
                            return;
                        }
                        that.load($(aa[0]).attr("href"));
                    });
                    if (typeof options.fnInitComplete === "function"){
                        options.fnInitComplete();
                    }
                },
                error:  that.loadError
            });
        }
    }
    
    return that;
})    
    