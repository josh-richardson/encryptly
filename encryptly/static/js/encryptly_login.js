/**
 * Created by joshua on 09/03/17.
 */

//Large AJAX post function
var currentState = 0;
var previousData = null;
$("#login").click(function () {
    //If we're in state 0, user hasn't entered U/N & PW
    if (currentState == 0) {
        $.post(Urls.user_login(), {
            username: $("#id_username").val(),
            password: $("#id_password").val()
        }).done(function (data) {
            handleLoginResponse(data);
        });
    } else if (currentState == 1) {
        //User has logged in, but 2FA is required. Send the username and the 2FA key to the server
        $.post(Urls.user_login(), {
            username: $("#id_username").val(),
            two_factor: $("#id_2fa").val()
        }).done(function (data) {
            handleLoginResponse(data);
        });
    } else if (currentState == 2) {
        //The user has passed 2FA or it's not required. Decrypt the challenge phrase sent by the server with the user's decryption key, and send it to the server.
        var privateKey = CryptoJS.AES.decrypt(previousData.private_key, $('#id_decryption_key').val()).toString(CryptoJS.enc.Utf8);
        var challengePhrase = previousData.challenge_phrase;
        var crypt = new JSEncrypt();
        crypt.setPrivateKey(privateKey);
        var decryptedChallenge = crypt.decrypt(challengePhrase);
        if (!decryptedChallenge) {
            //If we failed, notify the user
            showError("Unable to decrypt your private key - are you sure you entered the correct decryption key?");
        } else {
            //If we were successful, attempt the final step of the login process.
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
    //If we logged in, go to the messaging interface.
    if (data.logged_in) {
        window.location.replace(Urls.test_main());
    }

    //Set a global variable so the latest set of data can be accessed in the button press function
    previousData = data;

    //If there was an error message show it and exit.
    var errorMessage = data.error_message;
    if (errorMessage != null) {
        showError(errorMessage);
        return;
    }


    //If the username and password were correct then hide the inputs
    if (data.authenticated) {
        $("#initial_authenticate").fadeOut("slow", function () {
            //Either show 2FA or challenge phrase prompt depending on data from server
            if (data.two_factor && !data.passed_two_factor) {
                //Show 2FA
                currentState = 1;
                $("#two_fa_authenticate").fadeIn("slow");
            } else if (data.challenge_phrase) {
                //If the user passed 2FA, hide the relevant interface and show the decryption one, else just show the decryption interface
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

//Display an error to the user
function showError(errorMessage) {
    $('.alert-danger').html(errorMessage);
    var errorElement = $('#ajax_error');
    if (!errorElement.is(":visible")) {
        errorElement.fadeIn("slow");
    }
}