
// XXX: Handle pagination

var COMM = (function(options){
    "use strict"
    
    var params = {
        can_submit: options.can_submit || false,
        container:  "#" + (options.container || "comments"),
        type:       options.type,
        resource:   null,
        // XXX: Fix urls 
        user_comments_url:  function(username) {
            return "/user/" + username + "/comments";
        },
        request_comments_url:   function(res) {
            return "/comments/json?request=" + res;
        },
        max_pages:  5,
        half:       Math.floor(5/2)
    },
    utils   = {
        "has_prev":     function(page, total) {
            if (total > params.max_pages && page > 1){
                return true;
            }
            return false;
        },
        "prev_page":    function(page, total) {
            if (!utils.has_prev(page, total)){
                return null;
            }
            return page - 1;
        },
        "has_next":     function(page, total) {
            if (total > params.max_pages && total > page){
                return true;
            }
            return false;
        },
        "next_page":    function(page, total) {
            if (!utils.has_next(page, total)) {
                return null;
            }
            return page + 1;
        },
        "start":        function(page, total) {
            if (!(total > params.max_pages && page > params.half+1)){   // left
                return 1;
            } else if (!(total > params.max_pages && total- page > params.half)){   // right
                return total - params.max_pages + 1;
            } else {
                return page - params.half;
            }
        },
        "end":          function(page, total) {
            if (!(total > params.max_pages && total- page > params.half)) {  // right
                return total;
            } else if (!(total > params.max_pages && page > params.half+1)){  // left
                return params.max_pages;
            } else {
                return page + params.half;
            }
        },
    },
    aux     = {
        init_process:   function(){
            $(".alert-error").empty().hide();
        },
        stop_process:   function(){
            $(".wait").hide();
        }
    },
    dom = {
        item:   function(text, username, date, date_label, is_first) {
            var c   = 'e-comment-first';
            //if (is_first === undefined || is_first === false){
            //    c   = 'e-comment-item';
            //}
            var s   = '<div class="full-description ' + c + ' clearfix">';
            s   += '    <div>' + text + '</div>';
            s   += '    <div class="pull-right">';
            s   += '        <div class="e-request-time" title="' + date_label + '">' + date + '</div>';
            s   += '        <div class="pull-right"><a href="/user/' + username + '">' + username + '</a></div>';
            s   += '    </div>';
            s   += '</div>';
            return s;
        },
        submit_form:    function(text) {
            var t   = text || "";
            var s   = '<div id="comment_holder"></div>';
            s   += '<textarea rows="2" placeholder="Write a comment" class="span6" id="id_comment" name="comment">'+ t +'</textarea>';
            s   += '<div class="e-alert e-alert-inline alert-error pull-left" style="display: none" id="submit_error"></div>';
            s   += '<button id="submit_comment" class="btn btn-primary pull-right">Submit Comment</button>';
            s   += '<img src="/media/img/spinner_small.gif" id="comment_spinner" style="display: none" class="wait e-button-spinner pull-right"/>';
            return s;
        },
        paginator:      function(pi) {
            // Returns paginator
            var s   = '<div class="pagination e-comments-paging">';
            s   += '    <ul>';
            if (pi.has_prev) {
                s   += '<li><a href="?page=' + pi.prev_page + '" class="prev">Previous</a></li>'
            }
            var p;
            for (p = pi.start; p <= pi.end; p++) {
                if (p === pi.page){
                    s   += '<li class="current page active"><a>' + p + '</a></li>';
                } else {
                    s   += '<li><a href="?page=' + p + '" class="page">' + p + '</a></li>';
                }
            }
            if (pi.has_next) {
                s   += '<li><a href="?page=' + pi.next_page + '" class="next">Next</a></li>'
            }
            s   += '</ul>';
            s   += '</div>';
            return s;
        },
        wait:   '<img src="/media/img/spinner_small.gif" class="wait"/>',
        error:  function(msg) {
            return '<div class="e-alert alert-error">' + msg + '</div>';
        }
    };
    

    // Public object
    var that = {
        load_error:   function(jqXHR, textStatus, errorThrown) {
            var msg = that.error_msg(jqXHR, textStatus, errorThrown);
            $(params.container).html(dom.error(msg));
        },
        submit_error: function(jqXHR, textStatus, errorThrown) {
            var msg = that.error_msg(jqXHR, textStatus, errorThrown);
            $("#submit_error").html(msg).show();
        },
        error_msg:  function(jqXHR, textStatus, errorThrown) {
            aux.stop_process();
            var msg = errorThrown;
            try {
                var error  = JSON.parse(jqXHR.responseText).error;
                if ( error !== undefined) {
                    msg = error;
                };
            } catch(err) {}
            return msg;
        },
        load_comments:  function(res){
            
            params.resource = res;
            
            $.ajax({
                url:    params.request_comments_url(res),
                type:   "GET",
                cache:  false,
                beforeSend: function() {
                    aux.init_process();
                    $(params.container).html(dom.wait);
                },
                success:    function(data) {
                    aux.stop_process();
                    
                    var comments    = data.data.comments;
                    if ( comments === undefined){
                        return; // XXX: Handle properly!
                    }
                    var i;
                    var s   = "";
                    for (i = 0; i < comments.length; i++){
                        var com = comments[i];
                        var is_first    = false;
                        if (i === 0){
                            is_first = true;
                        }
                        s   += dom.item(com.text, com.username, com.hdate, com.utcdate, is_first);
                    }
                    s   += that.show_pages(data);
                    if (params.can_submit){
                        s   += dom.submit_form();
                    }
                    $(params.container).html(s);
                    
                    $("#submit_comment").unbind()
                        .click(that.submit_form);
                },
                error:  that.load_error
            });
        },
        show_pages:     function(data){
            if (data.data.paging === undefined){
                return "";
            }
            var page    = data.data.paging.page;
            var total   = data.data.paging.total;
            var page_info   = {
                "page":    page,
                "total":   total,
                "has_prev":     utils.has_prev(page, total),
                "prev_page":    utils.prev_page(page, total),
                "next_page":    utils.next_page(page, total),
                "has_next":     utils.has_next(page, total),
                "start":        utils.start(page, total),
                "end":          utils.end(page, total),
            }
            return dom.paginator(page_info);
        },
        submit_form:    function(){
            
            $.ajax({
                url:    "/comments/add/json?request=" + params.resource,
                type:   "POST",
                data:   {
                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                    "comment":      $("textarea[name=comment]").val()
                },
                cache:  false,
                beforeSend: function() {
                    aux.init_process();
                    $("#comment_spinner").show();
                },
                success:    function(data) {
                    aux.stop_process();
                    //that.append_comment(data)
                    that.load_comments(params.resource);
                },
                error:  that.submit_error
            })
        }
        //append_comment: function(data){
        //    // Not a very good idea!
        //    if (data.data === undefined){
        //        return;
        //    }
        //    $("#comment_holder").html(dom.item(com.text, com.username, com.hdate, com.utcdate, false));
        //}
    }
    
    return that;
})
