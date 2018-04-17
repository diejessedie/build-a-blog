def invalid_email(email):
    
    invalid_email.error = ''
    
    if email.count("@") != 1 or email.count(".") != 1 or not (2 < len(email) < 35):
            invalid_email.error = 'Invalid email. Must contain "@" and ".", must be 3-20 characters in length, no spaces.'
    else:
        invalid_email.error = ''

    return invalid_email.error

    
def invalid_usrnm(usrnm):
    if ' ' in usrnm or not (4 < len(usrnm) < 21):
        invalid_usrnm.error = 'Invalid username, must be 5-20 characters in length, no spaces.'
    elif usrnm == '':
        invalid_usrnm.error = 'Field required.'
    else:
        invalid_usrnm.error = ''
    
    return invalid_usrnm.error

def invalid_psswrd(psswrd):
    if ' ' in psswrd or not (4 < len(psswrd) < 21):
        invalid_psswrd.error = 'Invalid password, must be 5-20 characters in length, no spaces.'
    elif psswrd == '':
        invalid_psswrd.error = 'Field required.'
    else:
        invalid_psswrd.error = ''
    
    return invalid_psswrd.error

def psswrd_mismatch(psswrd, confirm):
    if psswrd == confirm:
        psswrd_mismatch.error = ''
    else:
        psswrd_mismatch.error = 'Passwords do not match.'

    return psswrd_mismatch.error