import re

def validate_full_name(arg):
    full_name_regex = re.compile(r'^[a-zA-Z가-힇]{2,}$')
    return full_name_regex.match(arg)

def validate_email(arg):
    email_regex = re.compile(r'^[a-zA-Z0-9]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+$')
    return email_regex.match(arg)

def validate_password(arg):
    password_regex = re.compile(r'^(?=.+[a-z])(?=.+[A-Z])(?=.+\d)(?=.+[!@#$%^&*()-=_+])[a-zA-Z0-9`~!@#$%^&*()_+-=,./<>?]{6,25}$')
    return password_regex.match(arg)

def validate_phone_number(arg):
    phone_number_regex = re.compile(r'^01[1|2|5|7|8|9|0]-?[0-9]{3,4}-?[0-9]{4}$')
    return phone_number_regex.match(arg)