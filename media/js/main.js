

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


function format_error(error_msg, error_default, msg_only)
{
    var msg;
    try {
        msg = JSON.parse(error_msg).error;
    } catch(err) {
        msg = error_default;
    }
    if (msg_only === true)
        return msg;
    var s   = '<div class="alert alert-error" style="margin-top: 10px;">';
    s   += msg;
    s   += '</div>';
    return s;
}



