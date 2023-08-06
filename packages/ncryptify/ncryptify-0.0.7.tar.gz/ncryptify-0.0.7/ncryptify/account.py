from json import dumps, loads

import requests

import config
import ncryptify_exceptions as Exceptions


def get_account(token):
    url = config.NCRYPTIFY_URL + "/admin/account"

    args = {
        'simple': 'true',
        'proxy': url,
    }
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    r = requests.get(url, headers=headers, params=args)
    if r.status_code != 200:
        raise Exceptions.AccountNotFound(r.text, r.status_code)
    return loads(r.text)

