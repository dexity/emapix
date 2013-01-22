
// Requires:
//      mustache.js
//      paginator.js
//      list.js


var COMM    = (function(options){
    "use strict"
    
    var params = {
        $container:     options.container,
        templates:      options.templates,
        submitBaseUrl:  options.submitBaseUrl,
        commentStatus:  "#comment_status",
        submitBtn:      "#submit_comment",
        fnSubmitCallback:   options.fnSubmitCallback
    }
    
    var list  = LIST(options),
        list_params = list.getParams();

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
    
    list.dom.submitSpinner = list.utils.compTmpl(params.templates.submitSpinner);
    list.dom.submitForm    = list.utils.compTmpl(params.templates.submitForm);
    
    list.initProcess    = function(){
        fn.initProcess();
        $(params.commentStatus).html(list.dom.submitSpinner());     // Show spinner
        $(params.submitBtn).attr({"disabled": "disabled"})    // Disable button
            .removeClass("disabled").addClass("disabled");
    };
    list.stopProcess    = function(){
        fn.initProcess();
        $(params.commentStatus).empty();
        $(params.submitBtn).removeClass("disabled").removeAttr("disabled");        
    };
    list.submitError    = function(jqXHR, textStatus, errorThrown) {
        // Error when comment is submitted
        var msg = list.errorMsg(jqXHR, textStatus, errorThrown);
        $(params.commentStatus).html(list.dom.error({"error": msg}));
    };   
    list.submitForm = function(){
        // Click event to submit form
        $.ajax({
            url:    params.submitBaseUrl, 
            type:   "POST",
            data:   {
                "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                "comment":      $("textarea[name=comment]").val()
            },
            cache:  false,
            beforeSend: function() {
                list.initProcess();
            },
            success:    function(data) {
                list.stopProcess();
                if (typeof params.fnSubmitCallback === "function"){
                    params.fnSubmitCallback(data);
                }
            },
            error:  list.submitError
        })
    };
    
    // Late binding
    options.fnInitComplete  = function(){
        if (params.submitBaseUrl !== undefined){
            list_params.$container.append(list.dom.submitForm({}));
        }
        
        // Register click event for comment submission
        $(params.submitBtn).unbind().click(list.submitForm);
    }   
    
    return list;
})


