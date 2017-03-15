/**
 * Created by joshua on 09/03/17.
 */

$("#id_public_key").removeAttr("required");
$("#id_private_key").removeAttr("required");


$("#register-next").click(function () {
    var form = $("#register_form");
    if (form.parsley().validate()) {
        form.fadeOut("slow", function () {
            $(".key-generation").fadeIn("slow");
            var crypt = new JSEncrypt({default_key_size: 4096});
            crypt.getKey(function () {
                console.log("Generated a key");
                $('#id_private_key').val(CryptoJS.AES.encrypt(crypt.getPrivateKey(), $("#decryption-key").val()).toString());
                $('#id_public_key').val(crypt.getPublicKey());

                //Submit using AJAX?
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