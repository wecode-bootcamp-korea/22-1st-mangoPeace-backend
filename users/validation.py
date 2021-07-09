import re

NICKNAME_REGEX     = r'^[a-zA-Z가-힇0-9]{1,8}$'
EMAIL_REGEX        = r'^[a-zA-Z0-9]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+$'
PASSWORD_REGEX     = r'^(?=.+[a-z])(?=.+[A-Z])(?=.+\d)(?=.+[!@#$%^&*()-=_+])[a-zA-Z0-9`~!@#$%^&*()_+-=,./<>?]{6,25}$'
PHONE_NUMBER_REGEX = r'^01[1|2|5|7|8|9|0][0-9]{3,4}[0-9]{4}$'

def validate_nickname(arg):
    return re.match(NICKNAME_REGEX, arg)

def validate_email(arg):
    return re.match(EMAIL_REGEX, arg)

def validate_password(arg):
    return re.match(PASSWORD_REGEX, arg)

def validate_phone_number(arg):
    return re.match(PHONE_NUMBER_REGEX, arg)