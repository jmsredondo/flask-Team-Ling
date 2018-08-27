$(document).ready(function () {
    var usernamePattern = new RegExp('^[a-z][a-z_]+$');
    var emailPattern = new RegExp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$');
    var passwordPattern = new RegExp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s]).{8,}$');

    $('#registerForm').submit(function (event) {
        submit = false;
        var username = $('input[name=username]').val();
        var email = $('input[name=email]').val();
        var password = $('input[name=password]').val();
        var password2 = $('input[name=password2]').val();

        var error = 0;
        if (!validate(username, usernamePattern)) {
            $('#username-errmsg').removeAttr('hidden');
            error += 1;
        } else {
            $('#username-errmsg').attr('hidden', 'hidden');
        }
        if (!validate(email, emailPattern)) {
            $('#email-errmsg').removeAttr('hidden');
            error += 1;
        } else {
            $('#email-errmsg').attr('hidden', 'hidden');
        }
        if (!validate(password, passwordPattern)) {
            $('#password-errmsg').removeAttr('hidden');
            error += 1;
        }else{
             $('#password-errmsg').attr('hidden', 'hidden');
        }
        if (password !== password2) {
            $('#conf-password-errmsg').removeAttr('hidden');
            error += 1;
        }else {
            $('#conf-password-errmsg').attr('hidden', 'hidden');
        }
        if (error > 1) {
            $('err-msg').removeAttr('hidden');
            submit = false;
        } else {
            submit = true;
        }
        return submit;
    });


})
;


function validate(field, pattern) {
    return pattern.test(field);
}