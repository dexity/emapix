
// Requires:
//      mustache.js
//      paginator.js
//      list.js


var COMM    = (function(options){
    "use strict"
    
    var params = {
        templates:      options.templates,
        submitBaseUrl:  options.submitBaseUrl
    }

    var list  = LIST(options);
    
    // Dirty code
    list.parent = function(name){
        var that    = this,
            method  = that[name];
        return function(){
            return method.apply(that, arguments);
        }
    }
    var fnnames  = ["initProcess", "stopProcess"],
        fn = {};   // Methods to subclass
    for (var i = 0; i < fnnames.length; i++){
        fn[fnnames[i]]  = list.parent(fnnames[i]);
    }
    
    //list.dom["submit_spinner"] = list.utils.compTmpl(params.templates.submit_spinner);
    //list.dom["submit_form"]    = list.utils.compTmpl(params.templates.submit_form);
    
    list.initProcess    = function(){
        fn.initProcess();
        //$(params.comment_status).html(dom.spinner());     // Show spinner
        //$(params.submit_btn).attr({"disabled": "disabled"})    // Disable button
        //    .removeClass("disabled").addClass("disabled");
    };
    list.stopProcess    = function(){
        fn.initProcess();
    }

                    //if (params.submit_base_url !== undefined){
                    //    $(params.container).append(dom.submit_form({}));
                    //}
                    //
                    //// Register click event for comment submission
                    //if (params.submit_id) {
                    //    $(params.submit_id).unbind()
                    //        .click(that.submit_form);
                    //}    
    
    return list;
})




//var COMM = (function(options){
//    "use strict"
//    
//    var params = {
//        container:      "#" + (options.container || "comments"),
//        submit_id:      (options.submit_id ? "#" + options.submit_id : null),
//        tmpl:           (options.tmpl_id ? $($("#" + options.tmpl_id).html()) : $({})),
//        comment_status: "#comment_status",
//        submit_btn:     "#submit_comment",
//        load_spinner:   "#" + (options.load_spinner || "load_spinner"),
//        type:           options.type,
//        resource:       null,
//        submit_base_url:    options.submit_base_url,
//        base_url:       options.base_url || "",
//        default_error:  "Service error. Please try again.",
//        fn_comment_created:   options.fn_comment_created,
//        paginator:      PAGES({})
//    };
//    
//    var utils   = {
//        page_url:   function(page){
//            return params.base_url + '&page=' + page;
//        }
//    },
//    aux     = {
//        comp_tmpl:      function(id){
//            // Compiles template with mustache
//            return Mustache.compile(params.tmpl.find(id).html());
//        },
//        init_process:   function(){
//            $(".alert-error").hide();   // Hide errors
//            $(params.comment_status).html(dom.spinner());     // Show spinner
//            $(params.submit_btn).attr({"disabled": "disabled"})    // Disable button
//                .removeClass("disabled").addClass("disabled");
//        },
//        stop_process:   function(){
//            $(params.load_spinner).empty();
//            $(params.comment_status).empty();
//            $(params.submit_btn).removeClass("disabled").removeAttr("disabled");
//        }
//    },
//    dom = {
//        item:           aux.comp_tmpl("#com_item"),
//        submit_form:    aux.comp_tmpl("#com_form"),
//        spinner:        aux.comp_tmpl("#com_spinner"),
//        load_spinner:   aux.comp_tmpl("#com_load_spinner"),
//        error:          aux.comp_tmpl("#com_error")
//    };
//    
//
//    // Public object
//    var that = {
//        load_error:   function(jqXHR, textStatus, errorThrown) {
//            // Error when comments are loaded
//            var msg = that.error_msg(jqXHR, textStatus, errorThrown);
//            $(params.container).html(dom.error({"error": msg}));
//        },
//        submit_error: function(jqXHR, textStatus, errorThrown) {
//            // Error when comment is submitted
//            var msg = that.error_msg(jqXHR, textStatus, errorThrown);
//            $(params.comment_status).html(dom.error({"error": msg}));
//        },
//        error_msg:  function(jqXHR, textStatus, errorThrown) {
//            aux.stop_process();
//            var msg = params.default_error;
//            try {
//                var js  = JSON.parse(jqXHR.responseText);
//                if ( js.error !== undefined) {
//                    msg = error;
//                } else if (typeof js.errors === "object") {
//                    var keys    = Object.keys(js.errors);
//                    if (keys.length > 0){
//                        msg = js.errors[keys[0]];
//                    }
//                };
//            } catch(err) {}
//            return msg;
//        },
//        load_comments:  function(url){
//            
//            var _url    = params.base_url;
//            if (url !== undefined){
//                _url    = url;
//            }
//            $.ajax({
//                url:        _url,
//                type:       "GET",
//                cache:      false,
//                beforeSend: function() {
//                    $(params.load_spinner).html(dom.load_spinner());
//                },
//                success:    function(data) {
//                    $(params.container).empty();
//                    aux.stop_process();
//                    
//                    var comments    = data.data.comments;
//                    if ( comments === undefined){
//                        return;     // No comments available
//                    }
//                    // Create paginator and set it in container
//                    for (var i = 0; i < comments.length; i++){
//                        var com = comments[i];
//                        var d   = {
//                            "text":         com.text,
//                            "username":     com.username,
//                            "date":         com.hdate,
//                            "date_label":   com.utcdate,
//                            "remove_url":   com.remove_url
//                        };
//                        var o   = $(dom.item(d));
//                        $(params.container).append(o);
//                        if (typeof params.fn_comment_created === "function"){
//                            params.fn_comment_created(o);
//                        }
//                    }
//                    if (data.data.paging !== undefined && params.paginator !== undefined){
//                        $(params.container).append(params.paginator.show_pages(params.base_url,
//                                                           data.data.paging.page,
//                                                           data.data.paging.total));
//                    }
//                    if (params.submit_base_url !== undefined){
//                        $(params.container).append(dom.submit_form({}));
//                    }
//                    
//                    // Register click events for pages
//                    $(".pagination li").click(function(e){
//                        e.preventDefault();
//                        var aa   = $(this).find("a");
//                        if (!(aa.length > 0 && $(aa[0]).attr("href"))) {
//                            return;
//                        }
//                        that.load_comments($(aa[0]).attr("href"));
//                    });
//                    // Register click event for comment submission
//                    if (params.submit_id) {
//                        $(params.submit_id).unbind()
//                            .click(that.submit_form);
//                    }
//                },
//                error:  that.load_error
//            });
//        },
//        submit_form:    function(){
//            
//            $.ajax({
//                url:    params.submit_base_url, 
//                type:   "POST",
//                data:   {
//                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
//                    "comment":      $("textarea[name=comment]").val()
//                },
//                cache:  false,
//                beforeSend: function() {
//                    aux.init_process();
//                },
//                success:    function(data) {
//                    aux.stop_process();
//                    if (data !== undefined && data.data !== undefined && data.data.comments_total !== undefined){
//                        $("#comments_badge").html(data.data.comments_total);
//                    }
//                    that.load_comments(utils.page_url("last"));    // Move to last page
//                },
//                error:  that.submit_error
//            })
//        }
//    }
//    
//    return that;
//})
