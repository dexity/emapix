

var month_days = {
    "JAN":  31,
    "FEB":  29,
    "MAR":  31,
    "APR":  30,
    "MAY":  31,
    "JUN":  30,
    "JUL":  31,
    "AUG":  31,
    "SEP":  30,
    "OCT":  31,
    "NOV":  30,
    "DEC":  31,
}

function set_error(error_msg, container)
{
    var c   = container;
    if (c === undefined)
        c   = $("#errors_container");
        
    var s   = '<div class="alert alert-error">';
    s   += '<a href="#" class="close" data-dismiss="alert">×</a>';
    s   += '<span id="error_msg">' + error_msg + '</span>';
    s   += '</div>';

    c.html(s);
}




