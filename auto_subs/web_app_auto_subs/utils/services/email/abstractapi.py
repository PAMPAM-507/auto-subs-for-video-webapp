import requests
from auto_subs.settings import API_KEY, API_URL, USE_ABS_API
import json


def validate_email(email: str) -> bool:

    if USE_ABS_API:

        response = requests.get(
            f"{API_URL}&email={email}")

        print(type(json.loads(response.content.decode())))
        print(json.loads(response.content.decode()))
        is_valid = is_valid_email(json.loads(response.content.decode()))

        return is_valid
    
    else:
        return True



def is_valid_email(data: dict) -> bool:

    print(data.get('is_valid_format'))
    if data.get('is_valid_format', False).get('value', False) and data.get('is_smtp_valid', False).get('value', False):

        # if not data.get('is_catchall_email').get('value', False) and not data.get('is_role_email').get('value', False) and data.get('is_free_email').get('value', False):
        return True

    return False
