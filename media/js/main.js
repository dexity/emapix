

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

function fadeOutErrors()
{
    $("input").focus(function(){
        $(".alert-error").fadeOut(1000);
    });
}

var b_month_change  = function(b_month, b_day) {
    
    $("select[name=b_month]").change(function(){
        var days    = '<option value="" selected="selected">Day</option>';
        if (this.value in month_days) {
            for (var i = 1; i< month_days[this.value]+1; i++) {
                days    += '<option value="' + i + '">' + i + '</option>'
            }
        }
        $("select[name=b_day]").html(days);
        $("select[name=b_day]").val(b_day);
    });
    $("select[name=b_month]").val(b_month).change();    
}


function set_error(error_msg, container)
{
    var c   = container;
    if (c === undefined){
        c   = $("#errors_container");
    }
    var s   = '<div class="alert alert-error">';
    s   += '<a href="#" class="close" data-dismiss="alert">×</a>';
    s   += '<span id="error_msg">' + error_msg + '</span>';
    s   += '</div>';

    c.html(s);
}


var format_error    = function(error_msg, error_default, msg_only){
    var msg;
    try {
        msg = JSON.parse(error_msg).error;
    } catch(err) {
        msg = error_default;
    }
    if (msg_only === true){
        return msg;
    }
    var s   = '<div class="alert alert-error" style="margin-top: 10px;">' + msg + '</div>';
    return s;
}


var error_msg   = function(jqXHR, textStatus, errorThrown) {
    var msg = errorThrown;
    try {
        var error  = JSON.parse(jqXHR.responseText).error;
        if ( error !== undefined) {
            msg = error;
        };
    } catch(err) {}
    return msg;
}

