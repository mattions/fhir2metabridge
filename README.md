# FHIR2Metadata bridge

Retrieving the data from the INCLUDE FHIR Data via the FHIR_resource.

Quick help:

```
 python fhir_trisomy_bridge.py --help
usage: fhir_trisomy_bridge.py [-h] --cavatica_token CAVATICA_TOKEN --cavatica_project CAVATICA_PROJECT
                              --include_fhir_authentication_cookie INCLUDE_FHIR_AUTHENTICATION_COOKIE

Retrieve metadata from teh INCLUDE Server and updates the metadata on the Cavatica Project

optional arguments:
  -h, --help            show this help message and exit
  --cavatica_token CAVATICA_TOKEN
                        You can find your developer token at https://cavatica.sbgenomics.com/developer/token
  --cavatica_project CAVATICA_PROJECT
                        The Cavatica project where the files are already imported from the INCLUDE Portal
  --include_fhir_authentication_cookie INCLUDE_FHIR_AUTHENTICATION_COOKIE
                        The Authorization cookie from the INCLUDE FHIR Server (https://include-api-fhir-
                        service.includedcc.org/) To obtain the cookie, open the Chorme or Firefox console, go to the
                        Application tab and copy the value contained in `AWSELBAuthSessionCookie-0`.
```


## How to retrieve the CAVATICA TOKEN

You can find your developer token at https://cavatica.sbgenomics.com/developer/token

Check the image in img/cavatica_auth_token.png to see a screenshot


## How to retrieve the CAVATICA Project

You can find your CAVATICA Project id on the top url

Check the image in img/cavatica_project_id.png to see a screenshot

## How to retrieve the FHIR cookie

The Authorization cookie from the INCLUDE FHIR Server (https://include-api-fhir-service.includedcc.org/) 
To obtain the cookie, open the Chorme or Firefox console, go to the Application tab and copy the value 
contained in `AWSELBAuthSessionCookie-0`.

Check the image in img/fhir_cookie_example.png to see how to identify the cookie

