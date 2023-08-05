import os
import random
import string
try:
    from urlparse import parse_qs, urlsplit
except ImportError:
    from urllib.parse import parse_qs, urlsplit

from django.contrib.auth.models import User

from oidc_provider.models import *


FAKE_NONCE = 'cb584e44c43ed6bd0bc2d9c7e242837d'
FAKE_RANDOM_STRING = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))


def create_fake_user():
    """
    Create a test user.

    Return a User object.
    """
    user = User()
    user.username = 'johndoe'
    user.email = 'johndoe@example.com'
    user.set_password('1234')

    user.save()

    return user


def create_fake_client(response_type):
    """
    Create a test client, response_type argument MUST be:
    'code', 'id_token' or 'id_token token'.

    Return a Client object.
    """
    client = Client()
    client.name = 'Some Client'
    client.client_id = '123'
    client.client_secret = '456'
    client.response_type = response_type
    client.redirect_uris = ['http://example.com/']

    client.save()

    return client


def create_rsakey():
    """
    Generate and save a sample RSA Key.
    """
    fullpath = os.path.abspath(os.path.dirname(__file__)) + '/RSAKEY.pem'

    with open(fullpath, 'r') as f:
        key = f.read()
        RSAKey(key=key).save()


def is_code_valid(url, user, client):
    """
    Check if the code inside the url is valid.
    """
    try:
        parsed = urlsplit(url)
        params = parse_qs(parsed.query)
        code = params['code'][0]
        code = Code.objects.get(code=code)
        is_code_ok = (code.client == client) and \
                     (code.user == user)
    except:
        is_code_ok = False

    return is_code_ok


class FakeUserInfo(object):
    """
    Fake class for setting OIDC_USERINFO.
    """

    given_name = 'John'
    family_name = 'Doe'
    nickname = 'johndoe'
    website = 'http://johndoe.com'

    phone_number = '+49-89-636-48018'
    phone_number_verified = True

    address_street_address = 'Evergreen 742'
    address_locality = 'Glendive'
    address_region = 'Montana'
    address_country = 'United States'

    @classmethod
    def get_by_user(cls, user):
        return cls()


def fake_sub_generator(user):
    """
    Fake function for setting OIDC_IDTOKEN_SUB_GENERATOR.
    """
    return user.email


def fake_idtoken_processing_hook(id_token, user):
    """
    Fake function for inserting some keys into token. Testing OIDC_IDTOKEN_PROCESSING_HOOK.
    """
    id_token['test_idtoken_processing_hook'] = FAKE_RANDOM_STRING
    id_token['test_idtoken_processing_hook_user_email'] = user.email
    return id_token


def fake_idtoken_processing_hook2(id_token, user):
    """
    Fake function for inserting some keys into token. Testing OIDC_IDTOKEN_PROCESSING_HOOK - tuple or list as param
    """
    id_token['test_idtoken_processing_hook2'] = FAKE_RANDOM_STRING
    id_token['test_idtoken_processing_hook_user_email2'] = user.email
    return id_token
