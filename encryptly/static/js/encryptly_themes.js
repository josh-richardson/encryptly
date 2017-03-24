$("#theme_dark").click(function () {
    $(".theme_remove").remove();
    $('head').append('<link href="/static/css/encryptly_theme_1.css" rel="stylesheet" class="theme_remove">');
    $.ajax({
        url:'/settheme/1/',
        type: 'GET',
        success: function() {
            console.log("Theme set: Dark");
}})});

$("#theme_def").click(function () {
    $(".theme_remove").remove();
    $.ajax({
        url:'/settheme/0/',
        type: 'GET',
        success: function() {
            console.log("Theme set: Default");
}})});
