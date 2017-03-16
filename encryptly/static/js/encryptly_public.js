/**
 * Created by joshua on 09/03/17.
 */


// window.Parsley.addAsyncValidator('username', function (xhr) {
//     var myResponseText = data.responseText;
//     console.log(myResponseText);
//     return 404 === xhr.status;
// }, '/user/exists/');
//'data-parsley-remote': "/user/exists/", 'data-parsley-remote-options': '{ "type": "POST", "data": { "username": "value" } }'
//
// window.Parsley.addValidator('username', {
//     validateString: function (value) {
//         var posting = $.post(
//
//             "/user/exists/",
//             {username: value}
//
//         );
//
//
//         return value.split('').reverse().join('') === value;
//     },
//     messages: {
//         en: 'This string is not the reverse of itself',
//     }
// });


Parsley.addAsyncValidator('validateUsername', function (xhr) {
    // Ideally the validation should be base on HTTP codes 200 and 404
    // But OctoberCMS framework always return 200. Throwing exceptions generated
    // a HTTP code 500 and during my test this causes a strange behaivor in parsley
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