/**
 * Created by joshua on 09/03/17.
 */

//Set up AJAX post requests so that they use Django CSRF tokens
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

//Add async parsley validator to validate usernames before AJAX form submission
Parsley.addAsyncValidator('validateUsername', function (xhr) {
    console.log(xhr.responseJSON);
    if (!xhr.responseJSON['allowed']) {
        alert("Too many requests have been made to the username validator. You will be redirected shortly...");
        return false;
    }
    return !xhr.responseJSON['exists'];
});


//Remove the required attribute from two inputs as they're auto-generated
$("#id_public_key").removeAttr("required");
$("#id_private_key").removeAttr("required");


//Registration form logic
$("#register-next").click(function () {
    var form = $("#register_form");
    // form.parsley().validate();
    form.parsley().whenValidate().done(function () {
        form.fadeOut("slow", function () {
            $(".key-generation").fadeIn("slow");
            var crypt = new JSEncrypt({default_key_size: 4096});
            crypt.getKey(function () {
                var decryptionKeyInput = $('#decryption-key');
                console.log("Generated a key");
                $('#id_private_key').val(CryptoJS.AES.encrypt(crypt.getPrivateKey(), decryptionKeyInput.val()).toString());
                $('#id_public_key').val(crypt.getPublicKey());
                decryptionKeyInput.remove();
                $('#decryption-key-confirm').remove();
                $('#register_form').submit();
            });

        });
    }).fail(function () {
        console.log("Remote verify failed");
    });
    form.parsley().validate();
});

$("#id_two_factor").change(function () {
    if (this.checked) {
        $("#id_mobile_number").attr("required", true);
    } else {
        $("#id_mobile_number").removeAttr("required");
    }
});


var currentState = 0;
$("#login").click(function () {
    if (currentState == 0) {
        $.post(Urls.user_login(), {
            username: $("#id_username").val(),
            password: $("#id_password").val()
        }).done(function (data) {
            handleLoginResponse(data);
        });

    }


});


function handleLoginResponse(data) {
    var errorMessage = data['error_message'];
    console.log(data);
    if (errorMessage != "") {
        var errorElement = $('.ajax_error');
        errorElement.first().html(errorMessage);
        if (!errorElement.is(":visible")) {
            errorElement.fadeIn("slow");
        }
        return;
    }


    if (data['authenticated']) {
        $("#initial_authenticate").fadeOut("slow", function () {
            if (data['2fa_required']) {
                $("#2fa_authenticate").fadeIn("slow");
            } else {
                $("#decryption_authenticate").fadeIn("slow");
            }
        });
    } else {
        $(".contact-form :input").prop("disabled", "false");
    }
}


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