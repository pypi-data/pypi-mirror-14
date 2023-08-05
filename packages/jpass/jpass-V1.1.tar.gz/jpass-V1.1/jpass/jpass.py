import common
import crypto

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from collections import OrderedDict
import glob
import os
import pickle

class Entry(object):

    def __init__(self, name, **kwargs):
        self.name = name
        self.fields = OrderedDict(kwargs)
    
    def write(self, key, path):
        """Serializes the object in a string and writes it to a file in an
        encrypted form.
            key -- the encryption key to use.
            path -- where to write the file.
        """
        serialized = pickle.dumps(self)
        ciphertext = crypto.encrypt(key, serialized, path)

    def __str__(self):
        """Causes the str() function to return the entry details."""
        s = "== %s ==\n" % self.name

        for j, k in self.fields.iteritems():
            if k:
                s += "%s: %s\n" % (j, k)
        return s

def read(key, path):
    """Attempt to decrypt an entry file and deserialize it, loading the object
    back into memory so that its attributes can be read.
        key -- the decryption key to try and use.
        path -- where to read from.
    """
    plaintext = crypto.decrypt(key, path)
    obj = pickle.loads(plaintext)
    return obj

def init():
    """Perform initialisation tasks, specifically:
        1. If there is no ~/.jpass directory, create one.
        2. If the user doesn't have a keyfile, walk them through creating one.
    """

    # If the ~/.jpass directory doesn't exist, create it and make sure that only
    # the current user can read its contents.
    if not os.path.isdir(common.DIRECTORY):
        os.mkdir(common.DIRECTORY)
        os.chmod(common.DIRECTORY, 0700)

    # If the user doesn't have a secret keyfile yet, make one.
    if not os.path.isfile(common.SECRET_KEYFILE_PATH):
        print "We must first create a keyfile before you can start using jpass."
        print "Please enter a strong passphrase for the keyfile."
        key = common.get_password()
        
        crypto.create_secret_keyfile(key, common.SECRET_KEYFILE_PATH)

def change_passwd():
    """Provides an intuitive interface for the user to change their password."""
    print "First, please unlock your keyfile."
    keyfile_data = common.get_keyfile_data()

    print "\n",

    print "Enter a new password for your keyfile."
    key = common.get_password(prompt="New password: ")
    crypto.encrypt(key, keyfile_data, common.SECRET_KEYFILE_PATH)

    print "\n",

    print "Done!"
    print "You will now have to use your new password to access your entries."

def edit_entry(name):
    """Provides an intuitive interface for the user to edit existing entries."""
    path = common.DIRECTORY + name

    if os.path.isfile(path):

        key = common.get_keyfile_data()
        print "\n",

        entry = read(key, path)
        print "As it stands, %s contains the following data:\n" % path
        print entry
        
        while 1:
            print "Choose a field to edit (case sensitive; enter nothing when done):"
            i = raw_input("<username/password/url/notes/...> ")

            if not i: break
            entry.fields[i] = raw_input("%s: " % i)
            
            print "\n",
            print "%s now contains the following data:\n" % path
            print entry
        
        entry.write(key, path)
        print "\n",
        print "Done!"

    else:
        print "Entry %s doesn't exist, so you can't edit it." % path

def list_entries():
    """Lists all .jpass files in ~/.jpass."""
    entries = glob.glob(common.DIRECTORY + "*.jpass")

    if entries:
        print "You have the following entry files in ~/.jpass:"

        # Take all of the paths, take their suffixes and print them each on a
        # new line.
        print "\n".join(e.rpartition("/")[-1] for e in entries)

    else:
        print "You have no entry files in ~/.jpass."

def read_entry(name):
    """Attempts to decrypt and load a .jpass file and show the user its
    attributes.
    """
    path = common.DIRECTORY + name

    if os.path.isfile(path):

        key = common.get_keyfile_data()

        print "\n",
        print read(key, path)
        print "Done!"

    else:
        print "Entry %s doesn't exist, so you can't read it." % path

def remove_entry(name):
    """Removes an entry from ~/.jpass (if it exists)."""
    path = common.DIRECTORY + name

    if os.path.isfile(path):
        os.remove(path)
        print "Successfully removed %s." % path
        print "Done!"
    else:
        print "Entry %s doesn't exist, so you can't remove it." % path

def store_entry(name):
    """Provides an intuitive interface for the user to create new entries."""
    path = common.DIRECTORY + name

    if not os.path.isfile(path):

        key = common.get_keyfile_data()
        print "\n",
        username = raw_input("username: ")
        password = raw_input("password: ")
        url = raw_input("url: ")
        notes = raw_input("notes: ")
        print "\n",


        e = Entry(name)
        e.fields["username"] = username
        e.fields["password"] = password
        e.fields["url"] = url
        e.fields["notes"] = notes

        more_fields = common.get_yes_no_response(
            "Would you like to add more fields? <y/n> ",
            err = "Please say either y (yes) or n (no)."
        )

        if more_fields:
                
            even_more_fields = True
            while even_more_fields:
                add_new_field(e)
                print "\n",
                even_more_fields = common.get_yes_no_response(
                    "Would you like to add another field? <y/n>  ",
                    err = "Please say either y (yes) or n (no)."
                )

        e.write(key, path)
        print "Done!"

    else:
        print "%s is already an entry!" % path
        print "You can edit it or delete it using the edit or remove tasks."

def add_new_field(e):
    """Creates a prompt for the user to add a new field to an entry object."""
    new_field_name = raw_input("Enter a name for the new field: ")
    new_field_value = raw_input("Enter the value for the new field: ")
    e.fields[new_field_name] = new_field_value

def main():
    ap = ArgumentParser(description="Manage your passwords.",
                        formatter_class=ArgumentDefaultsHelpFormatter)
    ap.add_argument("task", help="The task to perform.")
    ap.add_argument("--entry", "-e", help="The entry to work on.")
    args = ap.parse_args()

    # This dictionary maps 'task' keywords to their corresponding functions.
    tasks = {

        "change" : change_passwd,
        "changepasswd" : change_passwd,
        "passwd" : change_passwd,

        "change" : edit_entry,
        "edit" : edit_entry,
        "modify" : edit_entry,
        "tweak" : edit_entry,

        "list" : list_entries,
        "ls" : list_entries,

        "look" : read_entry,
        "read" : read_entry,
        "see" : read_entry,
        "view" : read_entry,

        "delete" : remove_entry,
        "remove" : remove_entry,
        "rm" : remove_entry,

        "create" : store_entry,
        "make" : store_entry,
        "store" : store_entry,
    }

    init()

    requested_task = args.task.lower()
    try:
        tasks[requested_task](args.entry + ".jpass")
    except TypeError:
        # If the function doesn't want a name to work with,
        # don't give it one.
        # TODO: perhaps a better way to do this...  
        tasks[requested_task]()
    except KeyError:
        # If the task that the user has given doesn't exist, tell
        # them.  
        print "No such task '%s'." % requested_task

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print "\n",
        print "Interrupt caught; exiting. Have a nice day!"
