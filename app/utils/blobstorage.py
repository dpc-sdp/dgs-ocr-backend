#!/usr/bin/env python3

# For to connect to blob storage ("state store" in Dapr terminology)
# and to get secrets (e.g. Form Recognizer key)
from dapr.clients import DaprClient

def push_blob(blob_name, value):
    with DaprClient() as d:
        storeName = 'coolfiles'
        try:
            print('Wait for dapr sidecar')
            d.wait(5) # Waits for sidecar, maximum 5 seconds
        except Exception as e:
            raise Exception("Seems like dapr sidecar was not up in time") from e
        print('Dapr sidecar is up, sending blob')
        d.save_state(store_name=storeName, key=blob_name, value=value)
        print('Blob is presumably saved')
