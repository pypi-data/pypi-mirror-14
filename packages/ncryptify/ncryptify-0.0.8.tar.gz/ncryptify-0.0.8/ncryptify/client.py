import datetime
import jwt
import encryption
import account


class Client:
    client_id = ""
    client_secret = ""
    issuer = ""
    subject = ""
    expires_in_minutes = 0
    renewal = -1
    token = ""

    def __init__(self, client_id='', client_secret='', issuer='', expires_in_minutes=0, subject='', token=''):
        self.client_id = client_id
        self.client_secret = client_secret
        self.issuer = issuer
        self.expires_in_minutes = expires_in_minutes
        self.subject = subject
        self.renewal = set_renewal(expires_in_minutes) if expires_in_minutes != 0 else -1
        if token != "":
            self.token = token
        else:
            self.token = self.construct_jwt(self.client_id, self.client_secret, self.issuer, self.expires_in_minutes, self.subject)

    @classmethod
    def init_with_client_id(cls, client_id, client_secret, issuer, expires_in_minutes, subject):
        token = cls.construct_jwt(client_id, client_secret, issuer, expires_in_minutes, subject)
        client = cls(client_id, client_secret, issuer, expires_in_minutes, subject, token)
        return client

    @classmethod
    def init_with_jwt(cls, jwt):
        client = cls(token=jwt)
        return client

    @staticmethod
    def construct_jwt(client_id, client_secret, issuer, expires_in_minutes, subject):
        now = datetime.datetime.utcnow()
        payload = {
            'iss': issuer,
            'sub': subject,
            'aud': client_id,
            'iat': now,
            'exp': now + datetime.timedelta(minutes=expires_in_minutes)
        }
        return jwt.encode(payload, client_secret, algorithm='HS256')

    def get_token(self):
        now = datetime.datetime.utcnow()
        if self. renewal != -1 and now > self.renewal:
            self.renewal = set_renewal(self.expires_in_minutes)
            self.token = self.construct_jwt(self.client_id, self.client_secret, self.issuer, self.expires_in_minutes, self.subject)
        return self.token

    def hide(self, value, key_name, hint, tweak=''):
        return encryption.fpe_hide(self.get_token(), value, key_name, hint, tweak)

    def unhide(self, value, key_name, hint, tweak=''):
        return encryption.fpe_unhide(self.get_token(), value, key_name, hint, tweak)

    def encrypt_blob(self, value, key_name):
        return encryption.encrypt_blob(self.get_token(), value, key_name)

    def decrypt_blob(self, value):
        return encryption.decrypt_blob(self.get_token(), value)

    def encrypt_file(self, key_name, plain_text_filename, cipher_text_filename):
        with open(plain_text_filename, 'rb') as plain_text_file, open(cipher_text_filename, 'wb') as cipher_text_file:
            encryption.enc_file(self.token, key_name, plain_text_file, cipher_text_file)

    def decrypt_file(self, cipher_text_filename, plain_text_filename):
        with open(cipher_text_filename, 'rb') as cipher_text_file, open(plain_text_filename, 'wb') as plain_text_file:
            encryption.dec_file(self.token, cipher_text_file, plain_text_file)

    def get_key(self, key_name):
        return encryption.get_key(key_name, self.get_token(), True)

    def delete_key(self, key_name):
        return encryption.delete_key(key_name, self.get_token())

    def get_account(self):
        try:
            return account.get_account(self.get_token())
        except Exception as e:
            raise e

    def get_random(self, length):
        return encryption.get_random(self.get_token(), length)


def set_renewal(minutes):
    when = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    # give 30 seconds grace
    when -= datetime.timedelta(seconds=30)
    return when

