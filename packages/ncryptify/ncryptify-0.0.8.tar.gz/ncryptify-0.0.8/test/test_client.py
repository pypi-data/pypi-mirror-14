__author__ = 'gkhunger'

import filecmp
import os
import json
import time

import pytest
import requests

import ncryptify.client as ncryptify
import ncryptify.config as config
import ncryptify.ncryptify_exceptions as Exceptions
import uuid
import binascii

NODE_ENCRYPTED_BLOB = None
NODE_ENCRYPTED_ID = None
NODE_ENCRYPTED_SECRET = None
NODE_ENCRYPTED_ISSUER = None
NODE_ENCRYPTED_SUBJECT = None
client = None


def setup_module(self):
    global NODE_ENCRYPTED_BLOB
    global NODE_ENCRYPTED_ID
    global NODE_ENCRYPTED_SECRET
    global NODE_ENCRYPTED_ISSUER
    global NODE_ENCRYPTED_SUBJECT
    global client

    if os.environ.get('NC_PRODUCTION'):
        NODE_ENCRYPTED_BLOB = "740000001076657273696f6e000100000002616c676f726974686d000e00000069642d6165733235362d47434d00026b65794964002500000032306265386361362d373639612d343938342d613533332d31306134343139383134323100056976000c00000000425a5c8a24e091f67fca9a4700173d630f9f3b6308390212d2124a8d94aea2378b2aa191429844c69491506f1550489a83397df7ab2babcce5dcd4ee02"
        NODE_ENCRYPTED_ID = os.environ['NCRYPTIFY_ID']
        NODE_ENCRYPTED_SECRET = os.environ['NCRYPTIFY_SECRET']
    else:
        NODE_ENCRYPTED_BLOB = "740000001076657273696f6e000100000002616c676f726974686d000e00000069642d6165733235362d47434d00026b65794964002500000039626363626364302d616164632d343330662d616564662d32336331653438316238323200056976000c00000000339fba53ba7e4c213d56025200d213e9bb0f95564fc8daeae76f978d5520fbb51c9f4e8d763d353b76ee0936e1826a7361f3f7ff4bd2f1537d38a1e27a"
        NODE_ENCRYPTED_ID = os.environ['NCRYPTIFY_ID']
        NODE_ENCRYPTED_SECRET = os.environ['NCRYPTIFY_SECRET']

    NODE_ENCRYPTED_ISSUER = "https://formfillastic.fitzysoft.com"
    NODE_ENCRYPTED_SUBJECT = "NODEJS-BLOB-KAT1-subject"
    client = ncryptify.Client.init_with_client_id(NODE_ENCRYPTED_ID,
                                                  NODE_ENCRYPTED_SECRET,
                                                  'myapp', 5, 'someone@myapp')


def make_key_name():
    return "not-a-uuid-" + str(uuid.uuid4())


def find_or_generate_fpe_key(token, name):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    url = config.NCRYPTIFY_URL + "/vault/keys"
    key_data = {
        'name': name,
        'usage': "fpe"
    }
    requests.post(url, headers=headers, data=json.dumps(key_data))
    # # Create an FPE.
    # find_or_generate_fpe_key(client.get_token(), fpe_key)


def test_hide_with_invalid_token():
    test_client = ncryptify.Client.init_with_client_id('adummyid',
                                                       'ZHVtbXkgZGF0YQ==',
                                                       'TEST_ISSUER', 5, 'test_subject')
    with pytest.raises(Exception) as excinfo:
        test_client.hide("test", "testKey", "alphabet")
    assert 'Unauthorized' in excinfo.value.message and excinfo.value.status_code == 401


def test_hide_unhide():
    pt = "test"
    ct = client.hide(pt, "testFpeKey", "alphabet")
    assert ct is not None
    assert pt != ct, 'FPE hide failed'

    dt = client.unhide(ct, "testFpeKey", "alphabet")
    assert dt is not None
    assert pt == dt, 'FPE unhide failed'

def test_hide_unhide_with_tweak():
    pt = "test"
    ct = client.hide(pt, "testFpeKey", "alphabet", "testtweak")
    assert ct is not None
    assert pt != ct, 'FPE hide with tweak failed'

    dt = client.unhide(ct, "testFpeKey", "alphabet", "testtweak")
    assert dt is not None
    assert pt == dt, 'FPE unhide with tweak failed'

def test_hide_unhide_with_mismatched_tweak():
    pt = "test"
    ct = client.hide(pt, "testFpeKey", "alphabet", "tweak1")
    assert ct is not None
    assert pt != ct, 'FPE hide with tweak failed'

    dt = client.unhide(ct, "testFpeKey", "alphabet", "tweak2")
    assert dt is not None
    assert pt != dt, 'FPE unhide with mismatched tweak failed'

def test_get_key():
    key_name = "test_Key"
    key = client.get_key(key_name)
    key_attr = ['account', 'devAccount', 'application', 'name', 'material', 'uri', 'meta', 'updatedAt', 'id',
                'createdAt', 'usage']
    assert (key['name'] == key_name)
    actualProps = [prop for prop in key]
    assert len(key_attr) == len(set(key_attr) & set(actualProps))


def test_get_random():
    random = client.get_random(16)
    assert len(random) == 16


def test_delete_existing_key():
    key_name = "dummyKeyForDeleting"
    client.get_key(key_name)
    res = client.delete_key(key_name)
    assert (res == 'Key Deleted Successfully')


def test_blob_encryption_without_blob_key():
    fpe_key = make_key_name()
    find_or_generate_fpe_key(client.get_token(), fpe_key)
    with pytest.raises(Exceptions.ErrorFetchingKey):
        client.encrypt_blob("test", fpe_key)


def test_delete_non_existent_key():
    key_name = "aNonExistentKey"
    with pytest.raises(Exceptions.KeyNotDeleted):
        client.delete_key(key_name)


# def test_hide_unhide_blob():
#     ct = client.hide("test string for NODEJS-BLOB-KAT1", "blob_Key", "blob")
#     assert client.unhide(ct, "blob_Key", "blob") == "test string for NODEJS-BLOB-KAT1"

def test_encrypt_decrypt_blob():
    ct = client.encrypt_blob("test string for NODEJS-BLOB-KAT1", "blob_Key")
    assert client.decrypt_blob(ct) == "test string for NODEJS-BLOB-KAT1"


@pytest.mark.skipif("os.environ.get('TEAMCITY') != '1'", reason="Not a local test")
def test_decrypt_node_encrypted_blob():
    test_client = ncryptify.Client.init_with_client_id(NODE_ENCRYPTED_ID,
                                                       NODE_ENCRYPTED_SECRET,
                                                       'https://formfillastic.fitzysoft.com', 5,
                                                       'NODEJS-BLOB-KAT1-subject')
    pt = test_client.decrypt_blob(binascii.unhexlify(NODE_ENCRYPTED_BLOB))
    assert pt == "test string for NODEJS-BLOB-KAT1"


def test_encrypt_file_with_fpe_key():
    fpe_key = make_key_name()
    find_or_generate_fpe_key(client.get_token(), fpe_key)
    path = "test/"
    filename = "testfile-small.txt"
    plain_text_filename = path + filename
    encrypted_text_filename = path + 'encrypted_' + filename

    open(encrypted_text_filename, 'w+')
    with pytest.raises(Exceptions.ErrorFetchingKey):
        client.encrypt_file(fpe_key, plain_text_filename, encrypted_text_filename)


def test_encrypt_decrypt_file():
    def test_encrypt_decrypt_file_helper(filename):
        path = "test/"
        plain_text_filename = path + filename
        encrypted_text_filename = path + 'encrypted_' + filename
        decrypted_text_filename = path + 'decrypted_' + filename

        open(encrypted_text_filename, 'w+')
        open(decrypted_text_filename, 'w+')
        client.encrypt_file("blob_Key", plain_text_filename, encrypted_text_filename)
        client.decrypt_file(encrypted_text_filename, decrypted_text_filename)
        assert filecmp.cmp(plain_text_filename, decrypted_text_filename)
        os.remove(encrypted_text_filename)
        os.remove(decrypted_text_filename)

    test_encrypt_decrypt_file_helper('testfile-small.txt')
    test_encrypt_decrypt_file_helper('testfile-large.txt')
    test_encrypt_decrypt_file_helper('testfile-16.txt')
    test_encrypt_decrypt_file_helper('testfile-32.txt')
    test_encrypt_decrypt_file_helper('testfile-64.txt')
    test_encrypt_decrypt_file_helper('testfile-big.pdf')


def test_decrypt_node_encrypted_file():
    path = "test/"
    plain_text_filename = path + "testfile-small.txt"
    encrypted_text_filename = path + "node_encrypted_testfile.txt"
    decrypted_text_filename = path + "decrypted_node_encrypted_testfile.txt"

    open(encrypted_text_filename, 'w+')
    open(decrypted_text_filename, 'w+')
    client.encrypt_file("blob_Key", plain_text_filename, encrypted_text_filename)
    client.decrypt_file(encrypted_text_filename, decrypted_text_filename)
    assert filecmp.cmp(plain_text_filename, decrypted_text_filename)
    os.remove(decrypted_text_filename)


def test_get_account():
    account = client.get_account()
    assert account is not None
    assert account['id'] is not None
    assert account['id'].strip() != ""

@pytest.mark.skipif("os.environ.get('TEAMCITY') != '1'", reason="Not a local test")
def test_init_with_jwt():
    token = ncryptify.Client.construct_jwt(NODE_ENCRYPTED_ID, NODE_ENCRYPTED_SECRET, NODE_ENCRYPTED_ISSUER, 5,
                                           NODE_ENCRYPTED_SUBJECT)
    test_client = ncryptify.Client.init_with_jwt(token)
    pt = test_client.decrypt_blob(binascii.unhexlify(NODE_ENCRYPTED_BLOB))
    assert pt == "test string for NODEJS-BLOB-KAT1"


def test_token_renewal():
    # setup jwt that expires in 1 minute. It would have been good if we could specify the expiry in seconds
    # so that the delay could be shorter. Passing -1 to this function causes the hide operation to raise an exception,
    # the JWT is not valid.
    test_client = ncryptify.Client.init_with_client_id(NODE_ENCRYPTED_ID, NODE_ENCRYPTED_SECRET,
                                                       'myapp', 1, 'someone@myapp')
    # wait a little bit more than a minute, JWT should be renewed on the next hide call
    time.sleep(70)
    ct = test_client.hide("test", "testFpeKey", "alphabet")
    assert ct is not None
    assert ct != "test"


def test_fail_token_renewal():
    # setup a JWT that is expired (passing -1 as the expiry time does this)
    token = ncryptify.Client.construct_jwt(NODE_ENCRYPTED_ID, NODE_ENCRYPTED_SECRET,
                                           'https://formfillastic.fitzysoft.com', -1, 'NODEJS-BLOB-KAT1-subject')
    test_client = ncryptify.Client.init_with_jwt(token)
    failed = False
    try:
        test_client.decrypt_blob(binascii.unhexlify(NODE_ENCRYPTED_BLOB))
    except Exception as e:
        # This exception is raised, among other things, when jwt is not valid.
        assert 'Unauthorized' in e.message and e.status_code == 401
        failed = True
    assert failed
