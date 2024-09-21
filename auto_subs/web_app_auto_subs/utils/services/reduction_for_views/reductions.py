


def handle_errors_for_ChangePassword_view_with_post_method(new_password1, new_password2):
    if (new_password1 != new_password2):
            message = 'Новые пароли должны совпадать'

    elif ((len(new_password1) < 8) or (len(new_password2) < 8)):
        message = 'Ваш пароль должен содержать не менее 8 символов'

    elif ((new_password1.isdigit()) or (new_password2.isdigit())):
        message = 'Ваш пароль не может быть полностью цифровым'

    else:
        message = 'Ваш пароль не может быть часто используемым паролем, слишком похож на другую вашу личную информацию либо введен неправильный старый пароль'

    return message



def handle_redirect_for_ChangeUserInfo_view_with_get_method(choose_form):
    if choose_form == '1':
        return 'change_password'

    elif choose_form == '2':
        return 'change_email'