/**
 * Created by joshua on 19/03/17.
 */
//Set up AJAX post requests so that they use Django CSRF tokens
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


//Helper functions
function getCookie(e) {
    var o = null;
    if (document.cookie && "" != document.cookie)
        for (var n = document.cookie.split(";"), t = 0; t < n.length; t++) {
            var i = jQuery.trim(n[t]);
            if (i.substring(0, e.length + 1) == e + "=") {
                o = decodeURIComponent(i.substring(e.length + 1));
                break
            }
        }
    return o
}