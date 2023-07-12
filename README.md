# Form Recognizer PoC

## Purpose

Proof of concept for running a Python web app (API) on Azure as a wrapper around Azure Form Recognizer, to extract data of interest from insurance certificates.

## What is in this repo?

- `infra/` - Terraform for deploying the infrastructure
- `app/` - source code for the Python web app (API), including Dockerfile

See below for instructions about how to run it.

## Running unit tests

run all unittests
`python3 -m unittest discover -s tests -v`

```
$ cd app
$ python3 -m unittest tests/utils/test_date_parser.py -vvv
$ python3 -m unittest tests/test_field_builder.py -vvv
$ python3 -m unittest tests/services/required_validation_test.py -vvv
$ python3 -m unittest tests/services/maxlength_validation_test.py -vvv
```

## Running the app locally

You will need to configure Dapr a bit:

- Create a file `app/secrets-for-running-locally/formrecognizer.secret.json` with the following content (but with placeholders filled in based on the Form Recognizer instance you'd like to run against):

```
{
  "endpoint": "https://{...}.cognitiveservices.azure.com/",
  "key": "..."
}
```

- In `app/components-for-running-locally/blobstorage.yaml`, fill in the `accountName` and `accountKey` field based on the Storage Account you'd like to run against.

Now you can build and run the app:

```
$ cd app
$ docker-compose build
$ docker-compose up
```

Then navigate your web browser to `http://localhost:5001/upload-form` to see the "troubleshooting UI" which is the fun bit.

## Deploying infra

Create a `.tfvars` file e.g.:

```
resource_group_name="forms-poc3"
azure_location="australiaeast"
blob_storage_account_name="formspocdocs3"
blob_storage_container_name="docs"
acr_name="formspocacr3"
fr_key_vault_name="formspockv3"
tags={
  "Client" = "Servian"
  "Purpose" = "Test"
  "Owner" = "patrick.conheady@servian.com"
}
```

Then run the Terraform:

```
$ cd infra
$ terraform init
$ az login # if you aren't already logged in
$ az account set -s "..." # Make sure you're pointing at the right subscription :-)
$ terraform apply -input=false -var-file your-name-here.tfvars
```

To view the "troubleshooting UI" in the cloud, go to the "Azure Container App" resource in the Azure portal and find its endpoint. The address will be something like `https://formsapp.blahblah-aaabbb.australiaeast.azurecontainerapps.io/upload-form`.

### Batch file Upload

Make the script executable

```
chmod +x batchupload-script.sh
```

Run Script

```
./batchupload-script.sh
```

### Batch file Upload Parallel

Make the script executable

```
chmod +x batchupload-script-parallel.sh
```

Run Script

```
./batchupload-script-parallel.sh
```
