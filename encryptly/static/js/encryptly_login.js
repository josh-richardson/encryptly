/**
 * Created by joshua on 09/03/17.
 */
var currentState = 0;
var previousData = null;
$("#login").click(function () {
    if (currentState == 0) {
        $.post(Urls.user_login(), {
            username: $("#id_username").val(),
            password: $("#id_password").val()
        }).done(function (data) {
            handleLoginResponse(data);
        });
    } else if (currentState == 1) {
        $.post(Urls.user_login(), {
            username: $("#id_username").val(),
            two_factor: $("#id_2fa").val()
        }).done(function (data) {
            handleLoginResponse(data);
        });
    } else if (currentState == 2) {
        var privateKey = CryptoJS.AES.decrypt(previousData.private_key, $('#id_decryption_key').val()).toString(CryptoJS.enc.Utf8);
        var challengePhrase = previousData.challenge_phrase;
        var crypt = new JSEncrypt();
        crypt.setPrivateKey(privateKey);
        var decryptedChallenge = crypt.decrypt(challengePhrase);
        if (!decryptedChallenge) {
            showError("Unable to decrypt your private key - are you sure you entered the correct decryption key?");
        } else {
            $.post(Urls.user_login(), {
                username: $("#id_username").val(),
                password: $("#id_password").val(),
                challenge_response: decryptedChallenge
            }).done(function (data) {
                handleLoginResponse(data);
            });
        }
    }
});


/**
 * @param {string} data.error_message
 * @param {boolean} data.authenticated
 * @param {boolean} data.two_factor
 * @param {boolean} data.passed_two_factor
 * @param {boolean} data.logged_in
 * @param {string} data.challenge_phrase
 * @param {string} data.private_key
 * @param {string} data.public_key
 */
function handleLoginResponse(data) {
    console.log(data);
    if (data.logged_in) {
        window.location.replace(Urls.test_main());
    }


    previousData = data;
    var errorMessage = data.error_message;
    if (errorMessage != null) {
        showError(errorMessage);
        return;
    }



    if (data.authenticated) {
        $("#initial_authenticate").fadeOut("slow", function () {
            if (data.two_factor && !data.passed_two_factor) {
                currentState = 1;
                $("#two_fa_authenticate").fadeIn("slow");
            } else if (data.challenge_phrase) {
                currentState = 2;
                if (data.passed_two_factor) {
                    $("#two_fa_authenticate").fadeOut("slow", function () {
                        $("#decryption_authenticate").fadeIn("slow");
                    });
                } else {
                    $("#decryption_authenticate").fadeIn("slow");
                }
            }
        });
    } else {
        showError("The request received a malformed response")
    }
}


function showError(errorMessage) {
    $('.alert-danger').html(errorMessage);
    var errorElement = $('#ajax_error');
    if (!errorElement.is(":visible")) {
        errorElement.fadeIn("slow");
    }
}