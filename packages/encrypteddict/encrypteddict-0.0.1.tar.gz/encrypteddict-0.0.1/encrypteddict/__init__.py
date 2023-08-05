import base64
import gpgme
import io
import os
import re


class UnsupportedEncryptionMethod(Exception):
    pass


class DecryptionError(Exception):
    pass


class crypter():

    def __init__(self, gpg_home=None):
        if gpg_home:
            os.environ['GNUPGHOME'] = gpg_home
        self.ctx = gpgme.Context()
        self.ctx.armor = False  # Use ASCII-armor output
        self.recipients = None

    def decrypt_gpg(self, value):
        try:
            encrypted_bytes = io.BytesIO('{}'.format(base64.b64decode(value)))
            encrypted_bytes.seek(0)
            decrypted_bytes = io.BytesIO()
            self.ctx.decrypt(encrypted_bytes, decrypted_bytes)
            return decrypted_bytes.getvalue()
        except gpgme.GpgmeError as e:
            raise DecryptionError(e)

    def decrypt_match_group(self, value):
        regex = re.compile('ENC\[(.*),(.*)\]')
        regex_result = regex.search(value.group(0))
        encryption_type = regex_result.group(1)
        if encryption_type == 'GPG':
            return self.decrypt_gpg(regex_result.group(2))
        else:
            raise UnsupportedEncryptionMethod('No way of handling {} encryption type'.format(encryption_type))

    def decrypt_all(self, decrypt_this):
        if type(decrypt_this) == dict:
            for key, value in decrypt_this.iteritems():
                decrypt_this[key] = self.decrypt_all(value)
            return decrypt_this
        elif type(decrypt_this) == list:
            return [self.decrypt_all(item_value) for item_value in decrypt_this]
        elif type(decrypt_this) == str:
            pattern = re.compile(r'ENC\[.*,.*\]')
            return pattern.sub(self.decrypt_match_group, decrypt_this)
        else:
            return decrypt_this

    def encrypt_gpg(self, value, recipients):
        try:
            keys = [ self.ctx.get_key(recipient) for recipient in recipients ]
            decrypted_bytes = io.BytesIO('{}'.format(value))
            encrypted_bytes = io.BytesIO()
            decrypted_bytes.seek(0)
            self.ctx.encrypt(keys, 1, decrypted_bytes, encrypted_bytes )
            return base64.b64encode(encrypted_bytes.getvalue())
        except gpgme.GpgmeError as e:
            raise DecryptionError(e)

    def encrypt_match_group(self, value):
        regex_result = value.group(2)
        encryption_type = value.group(1)
        if encryption_type == 'GPG':
            return 'ENC[GPG,{}]'.format(self.encrypt_gpg(regex_result, self.recipients))
        else:
            raise UnsupportedEncryptionMethod('No way of handling {} encryption type'.format(encryption_type))

    def encrypt_all(self, encrypt_this, recipients=None):
        if recipients:
            self.recipients = recipients
        if type(encrypt_this) == dict:
            for key, value in encrypt_this.iteritems():
                encrypt_this[key] = self.encrypt_all(value)
            return encrypt_this
        elif type(encrypt_this) == list:
            return [self.encrypt_all(item_value, recipients) for item_value in encrypt_this]
        elif type(encrypt_this) == str:
            pattern = re.compile(r'DEC::\((.*)\)\[(.*)\]')
            return pattern.sub(self.encrypt_match_group, encrypt_this)
        else:
            return encrypt_this
