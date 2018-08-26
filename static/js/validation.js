$(document).ready(function () {
    var usernamePattern = new RegExp('^[a-z][a-z_]+$');
    var emailPattern = new RegExp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$');
    var username = $('input[name=username]');
    var email = $('input[name=email]');
    username.on('input', function () {
        var val = $(this).val();
        if (val !== '') {
            console.log(ifUnique('username',val))
            if (usernamePattern.test(val) === true && ifUnique('username',val) === 0) {
                    validate(username, true, '');
            } else {
                validate(username, false, 'Invalid Username');
            }
        }
    });
    email.on('keyup', function () {
        var val = $(this).val();
        if (val !== '') {
            if (emailPattern.test(val) === true && ifUnique('email',val) === 0) {
                    validate(email, true, '');
            } else {
                validate(email, false, 'Invalid Email');
            }

        }
    })

});

function validate(element, result, message) {
    if (result === true) {
        element.removeClass('input-invalid');
        element.closest('.form-group').find('span').html(message);
    } else {
        element.addClass('input-invalid');
        element.closest('.form-group').find('span').html(message);
    }
}

function ifUnique(field, val) {
    $.ajax({
        url: '/validate',
        data: {'field':field,'value': val},
        dataType: 'JSON',
        success: function (result) {

        }
    });
}