

def make_hmac_signature(string, key):
    import hmac
    import hashlib
    import base64
    mac = hmac.new(str(key), str(string), hashlib.sha1)
    return base64.b64encode(mac.digest())


class BadSignature(Exception):
    pass


class SignatureExpired(Exception):
    pass

ARBITRARY_EPOCH = 1293840000   # number of seconds of 1/1/2011 after 1/1/1970


import datetime
import pytz


def get_secs_since_epoch():
    unix_epoch = pytz.utc.localize(datetime.datetime(1970, 1, 1))
    # arbitrary_epoch =
    now = pytz.utc.localize(datetime.datetime.now())
    now_in_secs = (now - unix_epoch).total_seconds()
    return now_in_secs - ARBITRARY_EPOCH


import base64


def sign(string, key):
    secs_since_epoch = get_secs_since_epoch()
    encoded_secs_since_epoch = base64.b64encode(unicode(secs_since_epoch))
    timestamped_data = string + '.' + encoded_secs_since_epoch
    signature = make_hmac_signature(timestamped_data, key)
    signed_string = timestamped_data + '.' + signature
    return signed_string


def unsign(string, key, max_age=10*60):
    timestamped_string, signature_in = string.rsplit('.', 1)
    signature_calced = make_hmac_signature(timestamped_string, key)
    if signature_calced != signature_in:
        raise BadSignature("signature '%s' does not match" % signature_in)
    string_res, timestamp = timestamped_string.rsplit('.', 1)
    decoded_timestamp = float(base64.b64decode(timestamp))
    secs_since_epoch = get_secs_since_epoch()
    time_diff = secs_since_epoch - decoded_timestamp
    if abs(time_diff) > max_age:
        raise SignatureExpired("decoded timestamp = '%s'; current seconds since epoch = '%s'; current - decoded = '%s'" % (decoded_timestamp, secs_since_epoch, time_diff))
    return string_res


def datetime_from_secs(secs):
    timestamp = secs + ARBITRARY_EPOCH
    return datetime.datetime.fromtimestamp(timestamp)
