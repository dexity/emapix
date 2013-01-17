

var PAGES   = (function(options){
    "use strict"  
    
    var params  = {
        base_url:   null,
        max_pages:  options.max_pages || 5,
        half:       0
    };
    params.half = Math.floor(params.max_pages/2);
    
    var utils   = {
        has_prev:     function(page, total) {
            if (total > params.max_pages && page > 1){
                return true;
            }
            return false;
        },
        prev_page:    function(page, total) {
            if (!utils.has_prev(page, total)){
                return null;
            }
            return page - 1;
        },
        has_next:     function(page, total) {
            if (total > params.max_pages && total > page){
                return true;
            }
            return false;
        },
        next_page:    function(page, total) {
            if (!utils.has_next(page, total)) {
                return null;
            }
            return page + 1;
        },
        start:        function(page, total) {
            if (!(total > params.max_pages && page > params.half+1)){   // left
                return 1;
            } else if (!(total > params.max_pages && total- page > params.half)){   // right
                return total - params.max_pages + 1;
            } else {
                return page - params.half;
            }
        },
        end:          function(page, total) {
            if (!(total > params.max_pages && total- page > params.half)) {  // right
                return total;
            } else if (!(total > params.max_pages && page > params.half+1)){  // left
                return params.max_pages;
            } else {
                return page + params.half;
            }
        },
    },
    dom =    {
        paginator:      function(p, t) {
            if (!params.base_url || t === 1) {
                return "";
            }
            // Returns paginator
            var s   = '<div class="pagination e-paging">',
            page_url   = function(page){
                var url = params.base_url,
                sep = "?";
                if (/\?/g.test(url)){   // Already has "?"
                    sep = "&";
                }
                return  url + sep + 'page=' + page;
            };
            s   += '    <ul>';
            if (utils.has_prev(p, t)) {
                s   += '<li><a href="' + page_url(utils.prev_page(p, t)) + '" class="prev">Previous</a></li>';
            }
            for (var pp = utils.start(p, t); pp <= utils.end(p, t); pp++) {
                if (pp === p){
                    s   += '<li class="current page active"><a>' + pp + '</a></li>';
                } else {
                    s   += '<li><a href="' + page_url(pp) + '" class="page">' + pp + '</a></li>';
                }
            }
            if (utils.has_next(p, t)) {
                s   += '<li><a href="' + page_url(utils.next_page(p, t)) + '" class="next">Next</a></li>'
            }
            s   += '</ul>';
            s   += '</div>';
            return s;
        }
    };
    
    var that    = {
        show_pages: function(url, page, total) {
            params.base_url = url;
            return dom.paginator(page, total);
        }
    }
    return that;
})