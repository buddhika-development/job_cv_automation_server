import re

# applicant name validation
# there only valid normal uses name patterns like 
# "Robert Doury", "R. Doury"
def applicant_name_validation(name):

    # name validation regex
    name_pattern = re.compile(r"^[A-Za-zÀ-ÿ](?:[A-Za-zÀ-ÿ\s\'\-\.]*(?![.\-\'\s]{2})(?<![\s\'\-\.])){1,48}[A-Za-zÀ-ÿ]$")

    # check applicant provided name is valid or not
    name_validation = re.match(name_pattern, name)

    return name_validation



# applicant phone number validation
# There are main three type of phone number
# 0762285559, +94762285559, or 0112345678
def applicant_phone_number_validation(phone_number):

    # phone number validation regex | pattern
    phone_pattern = re.compile(r"^(?:\+94|0)?(?:[1-9][1-9](?:[0-5]|[7-9])|[7][0-8])\d{6}$|^(?:\+94|0)?[7][0-8]\d{7}$")

    # check mobile number validatino
    phone_number_validation = re.match(phone_pattern, phone_number)

    return phone_number_validation



# applicant email address validation
def applicant_email_address_validation(email_address):

    # email address  pattern | regex
    email_pattern = re.compile(r"^(?![.])[a-zA-Z0-9.]+(?<!\.)@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z]{2,})+$")

    # applicant email address validation
    email_address_validation = re.match(email_pattern, email_address)

    return email_address_validation


# applicant uploaded cv validation
def applicant_cv_validation(cv_name):

    # pdf file validation regex | pattern
    filename_pattern = re.compile(r"^[A-Za-z0-9\s\-_À-ÿ]{1,100}\.pdf$", re.IGNORECASE)

    # applicant cv validation
    cv_validation = re.match(filename_pattern, cv_name)

    return cv_validation