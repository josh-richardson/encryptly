/**
 * Created by joshua on 09/03/17.
 */

Parsley.addAsyncValidator('validateUsername', function (xhr) {
    console.log(xhr.responseJSON);
    if (!xhr.responseJSON['allowed']) {
        alert("Too many requests have been made to the username validator. You will be redirected shortly...");
    }
    return !xhr.responseJSON['exists'];
});


$("#id_public_key").removeAttr("required");
$("#id_private_key").removeAttr("required");

$("#register-next").click(function () {
    var form = $("#register_form");
    form.parsley().validate();

    form.parsley().whenValidate()
        .done(function () {
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
        })
        .fail(function () {
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