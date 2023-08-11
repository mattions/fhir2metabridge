import argparse
import datetime
import requests
import simplejson

import sevenbridges as sbg
from sevenbridges.http.error_handlers import rate_limit_sleeper, maintenance_sleeper

class FHIR2Metadata:

    def __init__(self, cavatica_token, cavatica_project_id, fhir_auth_cookie):
        self.cavatica_token = cavatica_token
        self.cavatica_project = cavatica_project_id
        self.fhir_auth_cookie = fhir_auth_cookie
        self.CAVATICA_API_URL="https://cavatica-api.sbgenomics.com/v2"
        self.INCLUDE_FHIR= "https://include-api-fhir-service.includedcc.org/"
                                

    def main(self):
        """Retrieve the metadata from the INCLUDE FHIR Server"""
        
        api = sbg.Api(url=self.CAVATICA_API_URL, token=self.cavatica_token, advance_access=True, 
                        error_handlers=[rate_limit_sleeper, maintenance_sleeper])
        print("Retrieving data from Cavatica")
        files = api.files.query(project=self.cavatica_project).all()
        start = datetime.datetime.now()
        print(f"Starting this at: {start}")
        for fh in files:
            print(f"Working on file: {fh}")
            document_reference_url = fh.metadata['fhir_document_reference']

            if document_reference_url:
                print(document_reference_url)
                trisomy_state = self.get_trisomy_state(document_reference_url)
                if trisomy_state:
                    fh.metadata['sample_type'] = trisomy_state

                case_id = self.get_case_id(document_reference_url)
                if case_id:
                    fh.metadata['case_id'] = case_id
                    gender = self.get_gender(case_id)
                    if gender:
                        fh.metadata['gender'] = gender

                sample_id = self.get_sample_id(document_reference_url)
                if sample_id:
                    fh.metadata['sample_id'] = sample_id
                    age = self.get_age(sample_id)
                    if age:
                        fh.metadata['age'] = age
                    
                if trisomy_state or case_id or sample_id:
                    fh.save()
        stop = datetime.datetime.now()
        delta = stop - start
        print(f"Stop time: {stop}. Time taken: {delta}")

    def get_sample_id(self, document_reference_url):
        req = requests.get(document_reference_url, cookies = {"AWSELBAuthSessionCookie-0" : self.fhir_auth_cookie})
        req_j = req.json()
        try: 
            specimen = req_j['entry'][0]['resource']['context']['related'][0]['reference']
            query = f"{self.INCLUDE_FHIR}{specimen}"
            req = requests.get(query, cookies = {"AWSELBAuthSessionCookie-0" : self.fhir_auth_cookie})
            req_j = req.json()
            sample_id = ""
            for identifier in req_j['identifier']:
                if identifier['use'] == "official":
                    sample_id = identifier['value']
                    break
        except KeyError:
            print(f"WARN: Not able to extract sample id for {document_reference_url}")
            sample_id = None
        return sample_id
    
    def get_age(self, sample_id):
        req = requests.get(f"{self.INCLUDE_FHIR}Specimen/{sample_id}", cookies = {"AWSELBAuthSessionCookie-0" : self.fhir_auth_cookie})
        req_j = req.json()
        age = 0
        try:
            age = req_j['collection']['_collectedDateTime']['extension'][0]['extension'][3]['valueDuration']['value']
        except:
            age = None
        return age    

    def get_case_id(self, document_reference_url):
        req = requests.get(document_reference_url, cookies = {"AWSELBAuthSessionCookie-0" : self.fhir_auth_cookie})
        req_j = req.json()
        try:
            patient_number = req_j['entry'][0]['resource']['subject']['reference']
            query = f"{self.INCLUDE_FHIR}{patient_number}"
            req = requests.get(query, cookies = {"AWSELBAuthSessionCookie-0" : self.fhir_auth_cookie})
            req_j = req.json()
            case_id = ""
            for identifier in req_j['identifier']:
                if identifier['use'] == "official":
                    case_id = identifier['value']
                    break
        except KeyError:
            print(f"WARN: Not able to extract case id for {document_reference_url}")
            case_id = None
        return case_id

    def get_gender(self, case_id):
        req = requests.get(f"{self.INCLUDE_FHIR}Patient/{case_id}", cookies = {"AWSELBAuthSessionCookie-0" : self.fhir_auth_cookie})
        req_j = req.json()
        gender = ""
        try:
            gender = req_j['gender']
        except: 
            gender = None
        return gender

            
    def get_trisomy_state(self, document_reference_url):
        
        req = requests.get(document_reference_url, cookies = {"AWSELBAuthSessionCookie-0" : self.fhir_auth_cookie})
        
        try:
            req_j = req.json()
            patient_number = req_j['entry'][0]['resource']['subject']['reference']

            # Check if trosomy is present and confirmed
            # Condition --> `MONDO:000860`
            # verification-status=confirmed
            # patient/<number>
            # 
            # all url escaped looks like:
            # Condition?code=MONDO%3A0008608&subject=Patient%2F4927&verification-status=confirmed&_format=json
            
            query = f"{self.INCLUDE_FHIR}Condition?code=MONDO:0008608,MONDO:0700126,MONDO:0700030,MONDO:0700127,MONDO:0700128&verification-status=confirmed&subject={patient_number}&_summary=count&_format=json"
            print(query)
            req = requests.get(query, cookies = {"AWSELBAuthSessionCookie-0" : self.fhir_auth_cookie})
            req_j = req.json()
            total = req_j['total']
            trisomy_state=""
            if total == 0:
                trisomy_state = "D21"
            elif total == 1:
                trisomy_state = "T21"
        except KeyError:
            print(f"WARN: Not able to extract trisomy state for {document_reference_url}")
            trisomy_state = None
        return trisomy_state

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve metadata from teh INCLUDE Server and updates the metadata on the Cavatica Project')
    parser.add_argument("--cavatica_token", required=True, help="You can find your developer token at https://cavatica.sbgenomics.com/developer/token")
    parser.add_argument("--cavatica_project", required=True, help="The Cavatica project where the files are already imported from the INCLUDE Portal")
    parser.add_argument("--include_fhir_authentication_cookie", required=True, 
                        help="The Authorization cookie from the INCLUDE FHIR Server (https://include-api-fhir-service.includedcc.org/) \
                            To obtain the cookie, open the Chorme or Firefox console, go to the Application tab and copy the value \
                            contained in `AWSELBAuthSessionCookie-0`.")
    args = parser.parse_args()
    fhir2meta = FHIR2Metadata(args.cavatica_token, args.cavatica_project, args.include_fhir_authentication_cookie)
    fhir2meta.main()

