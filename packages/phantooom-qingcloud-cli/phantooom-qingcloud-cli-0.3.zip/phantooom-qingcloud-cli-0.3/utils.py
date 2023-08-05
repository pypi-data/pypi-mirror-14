import urllib
import base64
import hmac
from hashlib import sha256
from config import Config
import datetime
import requests
import json
from pprint import pprint

config = Config()
print config

def caculate_signature(method='GET', uri='/iaas/', url=''):
    string_to_sign = method + '\n' + uri + '\n' + url
    h = hmac.new(secret_access_key, digestmod=sha256)
    h.update(string_to_sign)
    sign = base64.b64encode(h.digest()).strip()
    signature = urllib.quote_plus(sign)


def explode_array(list_str, separator = ","):
    """
    Explode list string into array
    """
    if not list_str:
        return []
    return [item.strip() for item in list_str.split(separator) if item.strip() != '']

def send_request(action, directive):
    parmas = {
            'signature_version': 1,
            'signature_method': 'HmacSHA256',
            'version': 1,
            'access_key_id': config.access_key_id,
            'action': action,
            'time_stamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'zone': config.zone
          }

    for k, v in directive.iteritems():
        if v:
            if isinstance(v, list):
                for i in range(1,len(v)+1):
                    parmas[k + '.' + str(i)] = v[i-1]
            else:
                parmas[k] = v

    url_parmas = url_convert(parmas=parmas)

    url = signature(url_parmas = url_parmas)
    res = requests.get(url)

    if res.status_code==200:
        js_res = json.loads(res.content)
        print json.dumps(js_res, indent=4, sort_keys=True)
    else:
        print 'bad request'


def signature(method='GET', uri='/iaas/', url_parmas=''):
    string_to_sign = method + '\n' + uri + '\n' + url_parmas
    h = hmac.new(config.secret_access_key, digestmod=sha256)
    h.update(string_to_sign)
    sign = base64.b64encode(h.digest()).strip()
    signature = urllib.quote_plus(sign)
    return config.base_url + url_parmas + '&signature=' + signature


def url_convert(parmas=[]):
    for k, v in parmas.iteritems():
            if not isinstance(v, int):
                parmas[k] = urllib.quote_plus(v)
    sorted_parmas = sorted(parmas.iteritems(), key=lambda d: d[0])
    url_parmas = ''
    for k, v in sorted_parmas:
        url_parmas = url_parmas + '&' + k + '=' + str(v)
    return url_parmas[1:]