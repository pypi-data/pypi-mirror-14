import json

import requests
from bson import dumps, loads
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

import ncryptify_exceptions as exceptions
import config


blob_enc_type = 'id-aes256-GCM'
file_enc_type = 'id-aes256-GCM'
block_size = 64
METADATA_V1 = 1


def fpe_hide(token, value, key_name, hint, tweak):
    return _fpe('hide', token, value, key_name, hint, tweak)


def fpe_unhide(token, value, key_name, hint, tweak):
    return _fpe('unhide', token, value, key_name, hint, tweak)


def _fpe(cmd, token, value, key_name, hint, tweak):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    url = config.NCRYPTIFY_URL + "/crypto/" + cmd + "?keyName=" + key_name + "&hint=" + hint
    if len(tweak):
        url = url + "&tweak=" + tweak
    r = requests.post(url, headers=headers, data=value)
    if r.status_code != 200:
        if cmd=='hide':
            raise exceptions.HideRequestFailed(r.text, r.status_code)
        else:
            raise exceptions.UnhideRequestFailed(r.text, r.status_code)
    else:
        return r.text


def get_random(token, length):
    url = "{}{}{}".format(config.NCRYPTIFY_URL, "/vault/random?bytes=", length)
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise exceptions.ErrorFetchingRandom(r.text, r.status_code)
    return json.loads(r.text)['material'].decode('hex')


def get_key(key_name, token, create_key_flag):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    url = config.NCRYPTIFY_URL + "/vault/keys/" + key_name
    r = requests.get(url, headers=headers)
    if r.status_code == 404:
        if not create_key_flag:
            raise exceptions.KeyNotFound(r.text, r.status_code)
        else:
            return _create_key(key_name, token, True)
    elif r.status_code != 200:
        raise exceptions.ErrorFetchingKey(r.text, r.status_code)
    return json.loads(r.text)


def _create_key(key_name, token, retrieve_existing_key=False):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    url = config.NCRYPTIFY_URL + "/vault/keys"
    key_data = {
        'name': key_name
    }
    r = requests.post(url, headers=headers, data=json.dumps(key_data))
    if r.status_code == 409:
        if not retrieve_existing_key:
            raise exceptions.KeyAlreadyExists(r.text, r.status_code)
        else:
            headers = {"Authorization": "Bearer " + token}
            url = config.NCRYPTIFY_URL + "/vault/keys/" + key_name
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                raise exceptions.KeyAlreadyExists(r.text, r.status_code)
    elif r.status_code != 201:
        raise exceptions.KeyNotCreated(r.text, r.status_code)
    return json.loads(r.text)


def delete_key(key_name, token):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    url = config.NCRYPTIFY_URL + "/vault/keys/" + key_name
    r = requests.delete(url, headers=headers)
    if r.status_code != 204:
        raise exceptions.KeyNotDeleted(r.text, r.status_code)
    return 'Key Deleted Successfully'


def encrypt_blob(token, value, key_name):
    if key_name is None or len(key_name) == 0:
        key_name = 'defaultBlobEncryptionkey'
    key_data = get_key(key_name, token, True)
    if key_data['usage'] != "blob":
        raise exceptions.ErrorFetchingKey("Invalid key type found: " + key_data['usage'])
    key = key_data['material'].decode('hex')
    cipher_params = _get_cipher_params('blob')
    iv = get_random(token, cipher_params['ivSize'])
    ct = _encrypt(value, key, key_data['id'], iv, _get_cipher_params('blob'))
    return ct


def decrypt_blob(token, ct):
    # todo: is this efficient?  Is this decoding the bson, then reencoding it to get the len?
    md = loads(ct)
    md_len = len(dumps(md))
    md_bin = ct[:md_len]
    key_data = _get_key_by_id(token, md['keyId'])
    if key_data['usage'] != "blob":
        raise exceptions.ErrorFetchingKey("Invalid key type found: " + key_data['usage'])
    key = key_data['material'].decode('hex')
    pt = _decrypt(ct, key, md_bin, _get_cipher_params('blob'))
    return pt


def _encrypt(pt, key, key_id, iv, cipher_params):
    metadata = _create_metadata(METADATA_V1, cipher_params['alg'], iv, key_id)
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()

    if cipher_params['authTagSize'] > 0:
        encryptor.authenticate_additional_data(metadata)
        ct = metadata + encryptor.update(pt) + encryptor.finalize() + encryptor.tag[:cipher_params['authTagSize']]
    else:
        ct = metadata + encryptor.update(pt) + encryptor.finalize()
    return ct


def _decrypt(ct, key, md, cipher_params):
    iv = loads(md)['iv']
    tag = ct[len(ct)-cipher_params['authTagSize']:len(ct)]

    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    if cipher_params['authTagSize'] > 0:
        decryptor.authenticate_additional_data(md)
    data = ct[len(md):len(ct) - cipher_params['authTagSize']]
    pt = decryptor.update(data)
    pt_final = decryptor.finalize()
    if pt_final is not None:
        return pt_final + pt
    else:
        return pt


def enc_file(token, key_name, read_file, write_file):
    if key_name is None or len(key_name) == 0:
        key_name = 'defaultFileEncryptionkey'

    key_data = get_key(key_name, token, True)
    if key_data['usage'] != "blob":
        raise exceptions.ErrorFetchingKey("Invalid key type found: " + key_data['usage'])

    if key_data['material'] is not None:
        key = key_data['material'].decode('hex')
        cipher_params = _get_cipher_params('file')
        iv = get_random(token, cipher_params['ivSize'])
        metadata = _create_metadata(METADATA_V1, cipher_params['alg'], iv, key_data['id'])

        encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        ).encryptor()
        encryptor.authenticate_additional_data(metadata)
        write_file.write(metadata)

        while True:
            chunk = read_file.read(1024 * block_size)
            ct = encryptor.update(chunk)
            if len(chunk) == 0:
                break
            write_file.write(ct)

        encryptor.finalize()
        if cipher_params['authTagSize'] > 0:
            write_file.write(encryptor.tag[:cipher_params['authTagSize']])


def dec_file(token, read_file, write_file):
    # read metadata first to get key_id and iv
    chunk = read_file.read(1024 * block_size)
    md = loads(chunk)
    md_len = len(dumps(md))
    md_bin = chunk[:md_len]

    key_data = _get_key_by_id(token, md['keyId'])
    if key_data['usage'] != "blob":
        raise exceptions.ErrorFetchingKey("Invalid key type found: " + key_data['usage'])

    key = key_data['material'].decode('hex')

    iv = md['iv']

    # get the tag by changing the file object's position to 16th byte from the end of the file
    read_file.seek(-16,2)
    tag = read_file.read(1024 * block_size)

    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()
    decryptor.authenticate_additional_data(md_bin)

    cipher_params = _get_cipher_params('file')
    read_file.seek(md_len)
    while True:
        chunk = read_file.read(1024 * block_size)
        if len(chunk) == 0:
            break
        elif chunk[len(chunk)-cipher_params['authTagSize']: len(chunk)] == tag:
            chunk = chunk[:len(chunk)-cipher_params['authTagSize']]
        pt = decryptor.update(chunk)
        write_file.write(pt)

    pt_final = decryptor.finalize()
    if pt_final is not None:
        return pt_final + pt
    else:
        return pt


def _get_cipher_params (enc_type):
    if enc_type == 'file':
        if file_enc_type == 'id-aes256-GCM':
            return _aesgcm_cipher_params()
        else:
            return _aescbc_cipher_params()

    elif enc_type == 'blob':
        if blob_enc_type == 'id-aes256-GCM':
            return _aesgcm_cipher_params()
        else:
            return _aescbc_cipher_params()

    else:
        # use gcm as default.
        return _aesgcm_cipher_params()


def _create_metadata(version, alg_name, iv, keyId):
    metadata_doc = {
        'version': version,
        'algorithm': alg_name,
        'keyId': keyId,
        'iv': iv
    }
    return dumps(metadata_doc)


def _aesgcm_cipher_params():
    return {
        'alg': 'id-aes256-GCM',
        'ivSize': 12,
        'authTagSize':  16
    }


def _aescbc_cipher_params():
    return {
        'alg': "aes-256-cbc",
        'ivSize': 16,
        'authTagSize':  0
    }


def _get_key_by_id(token, key_id):
    url = config.NCRYPTIFY_URL + "/vault/keys/" + key_id
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise exceptions.KeyNotFound(r.text, r.status_code)
    return json.loads(r.text)
