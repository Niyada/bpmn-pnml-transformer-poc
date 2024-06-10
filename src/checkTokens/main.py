"""Implements the 'check_Tokens' HTTP Cloud Function.

This module defines a Google Cloud Function for RateLimiting the transform Endpoint.
"""
import firebase_admin
import functions_framework
from firebase_admin import credentials, firestore
from flask import jsonify
import os

# Firestore initialisieren
serviceAccountCertEncoded = os.getenv("GCP_SERVICE_ACCOUNT_CERTIFICATE")
cred = credentials.Certificate(serviceAccountCertEncoded)
firebase_admin.initialize_app(cred)
print(os.getcwd())
db = firestore.client()

os.env

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

