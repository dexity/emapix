

var COMM = (function(options){
    "use strict"
    
    var params = {
        can_submit: options.can_submit || "False",
        container:  options.container || "comments",
        type:       options.type,
        user_comments_url:  function(username) {
            return "/user/" + username + "/comments";
        },
        request_comments_url:   function(res) {
            return "/comments/json?request=" + res;
        }
    },
    utils   = {
        
    },
    dom = {
        item:   function(text, username, date, date_label) {
            s   = '<div class="full-description e-comment-first clearfix">';
            s   += '    <div>' + text + '</div>';
            s   += '    <div class="pull-right">';
            s   += '        <div class="e-request-time" title="' + date_label + '">' + date + '</div>';
            s   += '        <div class="pull-right"><a href="/user/' + username + '">' + username + '</a></div>';
            s   += '    </div>';
            s   += '</div>';
            return s;
        },
        submit_form:    function(text) {
            s   = '<textarea rows="2" placeholder="Write a comment" class="span6"></textarea>';
            s   += '<div class="e-alert-head e-alert-inline alert-error pull-left" style="display: none"></div>';
            s   += '<button class="btn btn-primary pull-right">Submit Comment</button>';
            s   += '<img src="/media/img/spinner_small.gif" id="comment_spinner" style="display: none" class="e-button-spinner pull-right"/>';
            return s;
        }
    }
    // Public object
    var that = {
        load_comments:  function(res){
            
            $.ajax({
                url:    params.request_comments_url(res),
                type:   "GET",
                cache:  false,
                success:    function(data) {
                },
                error:  function(jqXHR, textStatus, errorThrown) {
                }
            });
        }
    }
    
    return that;
})
