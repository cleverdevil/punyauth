import pecan
import hashlib
from webtest import TestApp


class GeneratePasswordHash(pecan.commands.base.BaseCommand):
    '''
    Generate a password hash for your password file
    '''

    def run(self, args):
        super(GeneratePasswordHash, self).run(args)
        self.load_app()
        salt = pecan.conf.passwords.salt
        password = input("Password: ")
        hashed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        print(hashed)
