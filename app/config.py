#!/usr/bin/env python3

# For to connect to blob storage ("state store" in Dapr terminology)
# and to get secrets form Azure (e.g. Form Recognizer key)
from dapr.clients import DaprClient
import os


def get_azure_form_recognizer_endpoint():
    # Handled by Dapr. When running locally, it's in a JSON file. When running in Azure, would be in Key Vault etc.
    with DaprClient() as client:
        return client.get_secret(store_name='form-recognizer-secret-store', key='endpoint').secret['endpoint']


def get_azure_form_recognizer_secret_key():
    # Key is handled by Dapr. When running locally, it's in a JSON file. When running in Azure, would be in Key Vault etc.
    with DaprClient() as client:
        return client.get_secret(store_name='form-recognizer-secret-store', key='key').secret['key']


def get_azure_form_recognizer_model_id():
    return os.environ.get('modelid').rstrip()


def get_db_uri():
    with DaprClient() as client:
        return client.get_secret(store_name='form-recognizer-secret-store', key='dburi').secret['dburi']


def get_api_key():
    with DaprClient() as client:
        return client.get_secret(store_name='form-recognizer-secret-store', key='apikey').secret['apikey']


def get_jwt_secret_key():
    with DaprClient() as client:
        return client.get_secret(store_name='form-recognizer-secret-store', key='jwtsecretkey').secret['jwtsecretkey']


def get_username():
    with DaprClient() as client:
        return client.get_secret(store_name='form-recognizer-secret-store', key='username').secret['username']


def get_password():
    with DaprClient() as client:
        return client.get_secret(store_name='form-recognizer-secret-store', key='password').secret['password']


def get_sn_username():
    with DaprClient() as client:
        return client.get_secret(store_name='form-recognizer-secret-store', key='snusername').secret['snusername']


def get_sn_password():
    with DaprClient() as client:
        return client.get_secret(store_name='form-recognizer-secret-store', key='snpassword').secret['snpassword']


def get_environment():
    return os.environ.get('environment', 'production')


def get_debugMode():
    return os.environ.get('debug', 'False')
