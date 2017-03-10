/**
 * Created by joshua on 09/03/17.
 */

// $(function() {
//     $(".checkbox-fix").each(function() {
//         $(this).append($(this).after($(this).attr("fix-text")));
//     });
// });
$("#id_public_key").removeAttr("required");
$("#id_private_key").removeAttr("required");



$("#register-next").click(function () {

    var form = $("#register_form");


    if (form.parsley().validate()) {
        form.fadeOut("slow", function () {
            $(".key-generation").fadeIn("slow");
        });
    }
// console.log(form.valid);
// if (form.valid) {

// }
})
;