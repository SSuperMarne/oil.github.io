/*
 *  Document   : op_auth_signup.js
 *  Author     : pixelcave
 *  Description: Custom JS code used in Sign Up Page
 */

var OpAuthSignUp = function() {
    // Init Sign Up Form Validation, for more examples you can check out https://github.com/jzaefferer/jquery-validation
    var initValidationSignUp = function(){
        jQuery('.js-validation-signup').validate({
            errorClass: 'invalid-feedback animated fadeInDown',
            errorElement: 'div',
            errorPlacement: function(error, e) {
                jQuery(e).parents('.form-group > div').append(error);
            },
            highlight: function(e) {
                jQuery(e).closest('.form-group').removeClass('is-invalid').addClass('is-invalid');
            },
            success: function(e) {
                jQuery(e).closest('.form-group').removeClass('is-invalid');
                jQuery(e).remove();
            },
            rules: {
                'username': {
                    required: true,
                    minlength: 3
                },
                'email': {
                    required: true,
                    email: true
                },
                'password1': {
                    required: true,
                    minlength: 6
                },
                'password2': {
                    required: true,
                    equalTo: '#signup-password'
                },
                'signup-terms': {
                    required: false
                }
            },
            messages: {
                'username': {
                    required: 'Придумайте имя пользователя (логин)',
                    minlength: 'Ваш логин должен содержать как минимум 3 символа'
                },
                'email': 'Пожалуйста, укажите верный E-mail',
                'password1': {
                    required: 'Пожалуйста, придумайте пароль',
                    minlength: 'Ваш пароль должен содержать минимум 6 символов'
                },
                'password2': {
                    required: 'Пожалуйста, повторите пароль',
                    minlength: 'Ваш пароль должен содержать минимум 6 символов',
                    equalTo: 'Пароли не совпадают'
                },
                'signup-terms': 'You must agree to the service terms!'
            }
        });
    };

    return {
        init: function () {
            // Init SignUp Form Validation
            initValidationSignUp();
        }
    };
}();

// Initialize when page loads
jQuery(function(){ OpAuthSignUp.init(); });