"""Implements the 'check_Tokens' HTTP Cloud Function.

This module defines a Google Cloud Function for RateLimiting the transform Endpoint.
"""
import tempfile
import base64
import firebase_admin
import functions_framework
import json
import re
from firebase_admin import credentials, firestore
from flask import jsonify
import os


GCP_SERVICE_ACCOUNT_CERTIFICATE_BASE64 = os.getenv( "GCP_SERVICE_ACCOUNT_CERTIFICATE" )
if( GCP_SERVICE_ACCOUNT_CERTIFICATE_BASE64 is None ):
    print( "Env var GCP_SERVICE_ACCOUNT_CERTIFICATE not found!" )

print('Base64:' + GCP_SERVICE_ACCOUNT_CERTIFICATE_BASE64)

GCP_SERVICE_ACCOUNT_CERTIFICATE_DECODED_BYTES = \
    base64.b64decode(GCP_SERVICE_ACCOUNT_CERTIFICATE_BASE64)

GCP_SERVICE_ACCOUNT_CERTIFICATE_DECODED_STRING = \
    GCP_SERVICE_ACCOUNT_CERTIFICATE_DECODED_BYTES.decode('utf-8')

print('Decoded String: ' + GCP_SERVICE_ACCOUNT_CERTIFICATE_DECODED_STRING)

cleaned_string = re.sub(r'[^\x20-\x7E]', ''
                        , GCP_SERVICE_ACCOUNT_CERTIFICATE_DECODED_STRING)

cleaned_string = cleaned_string.replace('\n', '').strip()
print('Cleaned String:  ' + cleaned_string)
json_data = json.loads(GCP_SERVICE_ACCOUNT_CERTIFICATE_DECODED_STRING, strict=False)


with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
    #temp_file.write(GCP_SERVICE_ACCOUNT_CERTIFICATE_DECODED_STRING.encode('utf-8'))
    #temp_file.write(cleaned_string.encode('utf-8'))
    json.dump(json_data, temp_file, ensure_ascii=False)
    temp_file_path = temp_file.name

with open(temp_file_path) as file:
    content = file.read()

print('content:' + content)

print(temp_file_path)
print('test')

cred = credentials.Certificate(temp_file_path)
firebase_admin.initialize_app(cred)
db = firestore.client()


@functions_framework.http
def check_tokens(request):
    """Check if there are tokens available in the Firestore database."""
    if db is None:
        return jsonify({"error": "No database available"}), 500

    doc_ref = db.collection("api-tokens").document("token-document")
    doc = doc_ref.get()
    if doc.exists:
        tokens = doc.to_dict().get("tokens", 0)
        if tokens <= 0:
            return jsonify({"error": "No tokens available"}), 400
        else:
            doc_ref.update({"tokens": tokens-1})
            return jsonify({"tokens": tokens-1}), 200
    else:
        return jsonify({"error": "No document available"}), 404

