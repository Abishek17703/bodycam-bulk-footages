import os
import json
import urllib.request
import urllib.parse

adc = json.load(open(os.path.expandvars(r'%APPDATA%\gcloud\legacy_credentials\abishek17703@gmail.com\adc.json')))
tok = json.loads(urllib.request.urlopen(urllib.request.Request(
    'https://oauth2.googleapis.com/token',
    data=urllib.parse.urlencode({
        'client_id': adc['client_id'],
        'client_secret': adc['client_secret'],
        'refresh_token': adc['refresh_token'],
        'grant_type': 'refresh_token'
    }).encode()
)).read())['access_token']

doc_id = '1xzU3MbBwtzc_sHQETNM-p_SdKtJXvVTu07Aih3JbuNM'
req = urllib.request.Request(
    f'https://www.googleapis.com/drive/v3/files/{doc_id}/permissions',
    data=json.dumps({'role': 'reader', 'type': 'anyone'}).encode('utf-8'),
    headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json'},
    method='POST'
)
res = json.loads(urllib.request.urlopen(req).read())
print('Shared:', res)
