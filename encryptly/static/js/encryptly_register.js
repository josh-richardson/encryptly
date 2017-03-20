/**
 * Created by joshua on 19/03/17.
 */
//Add async parsley validator to validate usernames before AJAX form submission
Parsley.addAsyncValidator('validateUsername', function (xhr) {
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
