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
import base64, hashlib, ast, os
from Crypto.Cipher import AES
class crypt(object):
    def __init__(self):
        self.BLOCK_SIZE = 32
        self.PADDING = '{'
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * self.PADDING
        self.EncodeAES = lambda c, s: base64.b64encode(c.encrypt(self.pad(s)))
        self.DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(self.PADDING)
    def encrypt(self, string, secret):
        secret = hashlib.sha224(secret).hexdigest()[:32]
        encoded = self.EncodeAES(AES.new(secret), string)
        return encoded
    
    def decrypt(self, string, secret):
        secret = hashlib.sha224(secret).hexdigest()[:32]
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
            f.write(self.crypt_wrapper.encrypt("{}", self.secret))
            f.close()
        f = open(filename, "r")
        unencrypted = self.crypt_wrapper.decrypt(f.read(), secret)
        self.dict = ast.literal_eval(unencrypted)
    def save(self):
        string = str(self.dict)
        encrypted = self.crypt_wrapper.encrypt(string, self.secret)
        f = open(self.filename, "w")
        f.write(encrypted)
        f.close()
        return self.dict
    #other stuff
    def keys(self):
        return self.dict.keys()
        
    def has_key(self, key):
        return key in self.dict
