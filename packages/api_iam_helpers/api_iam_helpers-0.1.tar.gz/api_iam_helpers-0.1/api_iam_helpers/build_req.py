import sys, os, base64, datetime, hashlib, hmac 

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

def get_signed_request(access_key,secret_key,region,api_id,token='',uri='/',parameters=''):
    # ************* REQUEST VALUES *************
    method = 'GET'
    service = 'execute-api'
    host = api_id + '.execute-api.eu-west-1.amazonaws.com'
    endpoint = 'https://' + host
    request_parameters = parameters
    canonical_uri = uri 
    canonical_querystring = request_parameters

    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope

    # ************* BUILD THE REQUEST ************
    canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
    signed_headers = 'host;x-amz-date'
    payload_hash = hashlib.sha256('').hexdigest()
    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
    string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request).hexdigest()

    signing_key = getSignatureKey(secret_key, datestamp, region, service)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    if len(token) > 0:
        headers = {'x-amz-date':amzdate, 'Authorization':authorization_header, 'x-amz-security-token':token}
    else:
        headers = {'x-amz-date':amzdate, 'Authorization':authorization_header}

    # ************* SEND THE REQUEST *************
    request_url = endpoint + canonical_uri + '?' + canonical_querystring

    return request_url, headers
