import requests
import hmac
import hashlib

GLOBAL_IDENTITY_SERVER = 'https://dlpgi.dlp-payments.com'


class GlobalIdentity:
    def __init__(self, app_key, global_identity_server=GLOBAL_IDENTITY_SERVER):
        self.global_identity_server = global_identity_server
        self.app_key = app_key

    def validate_application(self, client_app_key, client_secret_key,
                             resources, encrypt=True):
        secret_key = client_secret_key
        if encrypt:
            secret_key = hmac.new(
                str(client_secret_key),
                str(resources),
                hashlib.sha512).hexdigest()

        request = {
            'ApplicationKey': self.app_key,
            'ClientApplicationKey': client_app_key,
            'RawData': resources,
            'EncryptedData': secret_key,
        }

        response = requests.post(self.global_identity_server +
                                 '/api/Authorization/ValidateApplication',
                                 data=request)
        return response.json()

    def authenticate_user(self, email, password):
        request = {
            'ApplicationKey': self.app_key,
            'Email': email,
            'Password': password
        }

        response = requests.post(self.global_identity_server +
                                 '/api/Authorization/Authenticate',
                                 data=request)
        return response.json()

    def validate_token(self, token):
        request = {
            'ApplicationKey': self.app_key,
            'Token': token,
        }

        response = requests.post(
            self.global_identity_server +
            '/api/Authorization/ValidateToken',
            data=request)
        return response.json()

    def is_user_in_role(self, user_key, roles):
        request = {
            'ApplicationKey': self.app_key,
            'UserKey': user_key,
            'RoleCollection': list(roles)
        }

        response = requests.post(self.global_identity_server +
                                 '/api/Authorization/IsUserInRole',
                                 data=request)
        return response.json()
