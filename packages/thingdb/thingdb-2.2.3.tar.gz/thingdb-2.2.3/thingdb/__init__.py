#
#
#           .        .--.   _..._
#         .'|        |__| .'     '.   .--./)
#     .| <  |        .--..   .-.   . /.''\\
#   .' |_ | |        |  ||  '   '  || |  | |
# .'     || | .'''-. |  ||  |   |  | \`-' /
#'--.  .-'| |/.'''. \|  ||  |   |  | /("'`
#   |  |  |  /    | ||  ||  |   |  | \ '---.
#   |  |  | |     | ||__||  |   |  |  /'""'.\
#   |  '.'| |     | |    |  |   |  | ||     ||
#   |   / | '.    | '.   |  |   |  | \'. __//
#   `'-'  '---'   '---'  '--'   '--'  `'---'
#"thing" database - github/itslukej

#Imports
import base64, hashlib, ast, os, sys
from Crypto.Cipher import AES
class crypt(object):
    def __init__(self):
        self.BLOCK_SIZE = 32
        self.PADDING = '{'
        if sys.version_info >= (3,0):
            self.pad = lambda s: s + (self.BLOCK_SIZE - len(s.encode()) % self.BLOCK_SIZE) * self.PADDING #py3
            self.DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).decode().rstrip(self.PADDING) #py3
        else:
            self.pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * self.PADDING #py2
            self.DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(self.PADDING) #py2
        self.EncodeAES = lambda c, s: base64.b64encode(c.encrypt(self.pad(s)))
    def encrypt(self, string, secret):
        secret = hashlib.sha224(secret.encode()).hexdigest()[:32]
        encoded = self.EncodeAES(AES.new(secret), string)
        return encoded
    
    def decrypt(self, string, secret):
        secret = hashlib.sha224(secret.encode()).hexdigest()[:32]
        decoded = self.DecodeAES(AES.new(secret),string)
        return decoded

class thing(object):
    def __init__(self, filename="db.thing", secret="password"):
        #specify things
        self.crypt_wrapper = crypt()
        self.filename = filename
        self.secret = secret
        #
        if not os.path.isfile(self.filename):
            f = open(self.filename, "w+")
            if sys.version_info >= (3,0):
                f.write(self.crypt_wrapper.encrypt("{}", self.secret).decode())
            else:
                f.write(self.crypt_wrapper.encrypt("{}", self.secret))
            f.close()
        f = open(filename, "r")
        unencrypted = self.crypt_wrapper.decrypt(f.read(), secret)
        self.dict = ast.literal_eval(unencrypted)
    def save(self):
        string = str(self.dict)
        encrypted = self.crypt_wrapper.encrypt(string, self.secret)
        f = open(self.filename, "w")
        if sys.version_info >= (3,0):
            f.write(encrypted.decode())
        else:
            f.write(encrypted)
        f.close()
        return self.dict
    #other stuff
    def keys(self):
        return self.dict.keys()
        
    def has_key(self, key):
        return key in self.dict
        
    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __delitem__(self, key):
        del self.dict[key]
        
    def __contains__(self, key):
        return key in self.dict
        
    def __len__(self):
        return len(self.dict)
