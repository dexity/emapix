
// Requires mustache.js

var COMM = (function(options){
    "use strict"
    
    var params = {
        container:  "#" + (options.container || "comments"),
        submit_id: (options.submit_id ? "#" + options.submit_id : null),
        comment_status:    "#comment_status",
        submit_btn:     "#submit_comment",
        load_spinner:   "#" + (options.load_spinner || "load_spinner"),
        type:       options.type,
        resource:   null,
        submit_base_url:    options.submit_base_url || "",
        base_url:   options.base_url || "",
        default_error:  "Service error. Please try again.",
        paginator:  PAGES({})
    };
    
    var utils   = {
        page_url:   function(page){
            return params.base_url + '&page=' + page;
        }
    },
    aux     = {
        init_process:   function(){
            $(".alert-error").hide();   // Hide errors
            $(params.comment_status).html(dom.spinner);     // Show spinner
            $(params.submit_btn).attr({"disabled": "disabled"})    // Disable button
                .removeClass("disabled").addClass("disabled");
        },
        stop_process:   function(){
            $(params.load_spinner).empty();
            $(params.comment_status).empty();
            $(params.submit_btn).removeClass("disabled").removeAttr("disabled");
        }
    },
    dom = {
        item:   function(text, username, date, date_label, is_first) {
            var s   = '<div class="full-description e-comment-first clearfix">' +
                '    <div>' + text + '</div>' +
                '    <div class="pull-right">' +
                '        <div class="e-request-time" title="' + date_label + '">' + date + '</div>' +
                '        <div class="pull-right"><a href="/user/' + username + '">' + username + '</a></div>' +
                '    </div>' +
                '</div>';
            return s;
        },
        submit_form:    function(text) {
            var t   = text || "";
            var s   = '<div id="comment_holder"></div>' +
                '<textarea rows="2" placeholder="Write a comment" class="span6" id="id_comment" name="comment">'+ t +'</textarea>' +
                '<div id="comments_container">' +
                '   <div id="comment_status"></div>' +                 
                '   <button id="submit_comment" class="btn btn-primary pull-right">Submit Comment</button>' +
                '</div>';
            return s;
        },
        spinner:   '<img src="/media/img/spinner_small.gif" class="wait e-button-spinner"/>',
        load_spinner:   '<img src="/media/img/spinner_small.gif" class="wait e-button-spinner pull-right"/>',
        error:  function(msg) {
            return '<div class="e-alert e-alert-inline alert-error pull-left">' + msg + '</div>';
        }
    };
    

    // Public object
    var that = {
        load_error:   function(jqXHR, textStatus, errorThrown) {
            // Error when comments are loaded
            var msg = that.error_msg(jqXHR, textStatus, errorThrown);
            $(params.container).html(dom.error(msg));
        },
        submit_error: function(jqXHR, textStatus, errorThrown) {
            // Error when comment is submitted
            var msg = that.error_msg(jqXHR, textStatus, errorThrown);
            $(params.comment_status).html(dom.error(msg));
        },
        error_msg:  function(jqXHR, textStatus, errorThrown) {
            aux.stop_process();
            var msg = params.default_error;
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
        load_comments:  function(url){
            
            var _url    = params.base_url;
            if (url !== undefined){
                _url    = url;
            }
            
            $.ajax({
                url:        _url,
                type:       "GET",
                cache:      false,
                beforeSend: function() {
                    $(params.load_spinner).html(dom.load_spinner);
                },
                success:    function(data) {
                    aux.stop_process();
                    
                    var comments    = data.data.comments;
                    if ( comments === undefined){
                        return;     // No comments available
                    }
                    var s   = "";
                    // Create paginator and set it in container
                    for (var i = 0; i < comments.length; i++){
                        var com = comments[i];
                        var is_first    = false;
                        if (i === 0){
                            is_first = true;
                        }
                        s   += dom.item(com.text, com.username, com.hdate, com.utcdate, is_first);
                    }
                    if (data.data.paging !== undefined && params.paginator !== undefined){
                        s   += params.paginator.show_pages(params.base_url,
                                                           data.data.paging.page,
                                                           data.data.paging.total);
                    }
                    if (params.submit_base_url !== undefined){
                        s   += dom.submit_form();
                    }
                    $(params.container).html(s);
                    
                    // Register click events for pages
                    $(".pagination li").click(function(e){
                        e.preventDefault();
                        var aa   = $(this).find("a");
                        if (!(aa.length > 0 && $(aa[0]).attr("href"))) {
                            return;
                        }
                        that.load_comments($(aa[0]).attr("href"));
                    });
                    // Register click event for comment submission
                    if (params.submit_id) {
                        $(params.submit_id).unbind()
                            .click(that.submit_form);
                    }
                },
                error:  that.load_error
            });
        },
        submit_form:    function(){
            
            $.ajax({
                url:    params.submit_base_url, 
                type:   "POST",
                data:   {
                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                    "comment":      $("textarea[name=comment]").val()
                },
                cache:  false,
                beforeSend: function() {
                    aux.init_process();
                },
                success:    function(data) {
                    aux.stop_process();
                    if (data !== undefined && data.data !== undefined && data.data.comments_total !== undefined){
                        $("#comments_badge").html(data.data.comments_total);
                    }
                    that.load_comments(utils.page_url("last"));    // Move to last page
                },
                error:  that.submit_error
            })
        }
    }
    
    return that;
})
