try:
    from Crypto.Cipher import AES
except ImportError:
    print "jpass requires the pycrypto library to run."
    print "Please ensure that this is installed on your system."
    exit(1)

import hashlib
import os
import struct

class CryptoError(Exception):
    pass

def create_secret_keyfile(key, outfile, size=4096):
    """Creates the secret keyfile for the unified key setup.
       key     -- the encryption key used to encrypt the keyfile.
       size    -- the size of the keyfile in bytes (the greater, the better).
       outfile -- where to write the keyfile.
    """
    keyfile_data = os.urandom(size)
    encrypt(key, keyfile_data, outfile)

def raw_encrypt(key, data, chunk=1024*32):
    """Encrypts raw bytes.
        key   -- the encryption key to use.
        data  -- the data to encrypt.
        chunk -- the chunk size to use.
    """
    key = stretch_key(key)

    # Create random 16 byte initialization vector.  
    iv = os.urandom(16)
    size = len(data)

    # Using cipher block chain mode; effectively means each block of plaintext
    # is XORed with the previous block's ciphertext. This means each
    # ciphertext block is unique up to each point.  
    crypter = AES.new(key, AES.MODE_CBC, iv)
    encrypted = struct.pack("<Q", size) + iv + crypter.encrypt(SUCCESS_INDICATOR)

    for x in xrange(size // chunk + 1):
        td = data[x * chunk:(x + 1) * chunk]
        td = pad(td, 16, " ")
        encrypted += crypter.encrypt(td)

    return encrypted

def raw_decrypt(key, data, chunk=1024*32):
    """Decrypts raw bytes.
        key   -- the decryption key to attempt.
        data  -- the encrypted data to attempt to decrypt.
        chunk -- the chunk size to use.
    """
    key = stretch_key(key)
    retval = ""

    # Retrieve the original size and initialization vector.  
    origsize = struct.unpack("<Q", data[:struct.calcsize("<Q")])[0]
    data = data[struct.calcsize("Q"):]

    iv = data[:16]
    data = data[16:]

    crypter = AES.new(key, AES.MODE_CBC, iv)

    suc = crypter.decrypt(data[:len(SUCCESS_INDICATOR)])
    data = data[len(SUCCESS_INDICATOR):]
    
    # If this condition is true, we can assume with extremely high
    # probability that decryption was successful.  
    if suc != SUCCESS_INDICATOR:
        raise CryptoError("Decryption failed -- bad key or input data?")

    while 1:
        c = data[:chunk]
        data = data[chunk:]
        if not c:
            break
        retval += crypter.decrypt(c)
    
    return retval[:origsize]

def encrypt(key, data, outfile, file_permissions=0600):
    """Encrypts some data and writes it to a file 'outfile'.
        key     -- the encryption key to use.
        data    -- the data to encrypt.
        outfile -- the name of the file to output to.
    """
    with open(outfile, "wb") as f:
        # Write the initialization vector to the file.  
        f.write(raw_encrypt(key, data))

    # Assign file permissions.  
    os.chmod(outfile, file_permissions)

def decrypt(key, infile):
    """Decrypts some data from an 'infile' and returns the plaintext.
        key    -- the encryption key to use.
        infile -- the name of the file to take input from.
    """
    data = ""
    with open(infile, "rb") as f:
        data = f.read()
    
    return raw_decrypt(key, data)

def pad(data, bs, pad_char):
    """Pads a string. This is needed to transform a string of n bytes long
    to one whose length is equal to the specified `bs` argument.
        data     -- the data to pad.
        bs       -- the length of the new padded string (in bytes).
        pad_char -- the character to use for the padding
    """
    return data + (bs - len(data) % bs) * pad_char

def stretch_key(key, rounds=65536, salt="", algo=hashlib.sha256):
    """Stretches an encryption key by a default of 65536 rounds.
        key    -- the data to stretch.
        rounds -- how many iterations to spend rehashing the data.
        algo   -- the hash algorithm to use for the hashing.
    """
    stretched = key
    for _ in xrange(rounds):
        stretched = algo(stretched + key + salt).digest()
    return stretched

# This string is embedded in the 'header' of .jpass files, along with the file
# size and initialization vector (all of which are required for the encryption
# of entries).
#
# The purpose of the success indicator is as follows: when a .jpass file is
# decrypted, the header is examined for the success indicator string. Presence
# of the success indicator string means that we can assume, with extremely high
# probability, that decryption was successful. If the success indicator string
# is not found, then it means that decryption has failed. This is more than
# likely because the user has supplied an incorrect encryption key.
SUCCESS_INDICATOR = pad("SUCCESS", 16, " ")
