import crypto
import os

import getpass

DIRECTORY = os.path.expanduser("~") + os.path.sep + ".jpass" + os.path.sep
SECRET_KEYFILE_PATH = DIRECTORY + ".keyfile"

def get_keyfile_data():
    """Prompts the user for their password, decrypts their keyfile and returns
    its contents -- effectively returns the encryption key for all of the
    encrypted entry files in ~/.jpass.
    """
    keyfile_data = ""
    while not keyfile_data:
        password = get_password(confirm_prompt="")
        try:
            keyfile_data = crypto.decrypt(password, SECRET_KEYFILE_PATH)
        except crypto.CryptoError:
            print "Failed to unlock keyfile; bad password?"
    return keyfile_data

def get_password(prompt="Password: ", confirm_prompt="Confirm: ",
                 err="Passwords did not match.\n"):
    """Prompts the user for a password.
        prompt         -- the prompt to show the user.
        confirm_prompt -- the confirmation prompt to show the user. If null, do
                          do not confirm password input.
        err            -- the error message to print if the initial password
                          input and the confirm password input were not equal.
    """
    password = getpass.getpass(prompt)


    if confirm_prompt:
        while getpass.getpass(confirm_prompt) != password:
            print err
            password = getpass.getpass(prompt)

    return password

def get_yes_no_response(prompt, err="Invalid response.\n", yes="y", no="n"):
    """Gets a yes/no response from the user. Returns True if the user said yes,
    false if the user said no.
        prompt -- the prompt to show the user.
        err    -- the error message to print if the user does not respond with
                  either of the strings given by the keyword arguments `yes` or
                  `no`.
        yes    -- if the user inputs this string, return True.
        no     -- if the user inputs this string, return False.
    """
    response = ""
    while 1:
        response = raw_input(prompt)
        if    response == yes: return True
        elif  response == no:  return False
        else: print err
