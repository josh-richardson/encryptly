//Remove the old theme and insert the dark theme
$("#theme_dark").click(function () {
    $(".theme_remove").remove();
    $('head').append('<link href="/static/css/theme1.css" rel="stylesheet" class="theme_remove">');
    $.ajax({
        url: '/settheme/1/',
        type: 'GET',
        success: function () {
            console.log("Theme set: Dark");
        }
    })
});

//Just remove any old theme
$("#theme_def").click(function () {
    $(".theme_remove").remove();
    $.ajax({
        url: '/settheme/0/',
        type: 'GET',
        success: function () {
            console.log("Theme set: Default");
        }
    })
});
