/**
 * Created by joshua on 09/03/17.
 */

window.Parsley.addValidator('username', {
  validateString: function(value) {

    return value.split('').reverse().join('') === value;
  },
  messages: {
    en: 'This string is not the reverse of itself',
  }
});


    // var posting = $.post(
    //     "/flow/",
    //     { number: "2" }
    // );


$("#id_public_key").removeAttr("required");
$("#id_private_key").removeAttr("required");

$("#register-next").click(function () {
    var form = $("#register_form");
    if (form.parsley().validate()) {
        form.fadeOut("slow", function () {
            $(".key-generation").fadeIn("slow");
            var crypt = new JSEncrypt({default_key_size: 4096});
            crypt.getKey(function() {
                var decryptionKeyInput = $('#decryption-key');
                console.log("Generated a key");
                $('#id_private_key').val(CryptoJS.AES.encrypt(crypt.getPrivateKey(), decryptionKeyInput.val()).toString());
                $('#id_public_key').val(crypt.getPublicKey());
                decryptionKeyInput.remove();
                $('#decryption-key-confirm').remove();
                $('#register_form').submit();
            });

        });
    }
});


$("#id_two_factor").change(function () {
    if (this.checked) {
        $("#id_mobile_number").attr("required", true);
    } else {
        $("#id_mobile_number").removeAttr("required");
    }
});