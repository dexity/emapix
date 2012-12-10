

var COMM = (function(options){
    "use strict"
    
    var params = {
        container:  "#" + (options.container || "comments"),
        submit_btn: (options.submit_btn ? "#" + options.submit_btn : null),
        type:       options.type,
        resource:   null,
        submit_base_url:    options.submit_base_url || "",
        base_url:   options.base_url || "",
        paginator:  PAGES({})
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
                    aux.init_process();
                    $("#comment_spinner").show();
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
                    if (!params.submit_btn) {
                        $(params.submit_btn).unbind()
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
                    $("#comment_spinner").show();
                },
                success:    function(data) {
                    aux.stop_process();
                    if (data !== undefined && data.data !== undefined && data.data.comments_total !== undefined){
                        $("#comments_badge").html(data.data.comments_total);
                    }
                    that.load_comments(params.resource,
                                       params.request_comments_url(params.resource, "last"));    // Move to last page
                },
                error:  that.submit_error
            })
        }
    }
    
    return that;
})
