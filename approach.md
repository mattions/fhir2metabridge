


## General plan

Cavatica project to work from: https://cavatica.sbgenomics.com/u/mmattioni/include-htp-meta 

Main idea is:

for all the files in project:
 - extract `fhir_document_reference`

This is how it looks like:
```
// 20220714112305
// https://include-api-fhir-service.includedcc.org/DocumentReference?identifier=HTP.0012022d-c855-4087-9dde-c522f0632024.kallisto.abundance.tsv.gz&_format=json

{
  "resourceType": "Bundle",
  "id": "17a64462-2c75-49ff-9045-018f5876fccd",
  "meta": {
    "lastUpdated": "2022-07-14T09:22:59.484+00:00"
  },
  "type": "searchset",
  "total": 1,
  "link": [
    {
      "relation": "self",
      "url": "https://include-api-fhir-service.includedcc.org/DocumentReference?_format=json&identifier=HTP.0012022d-c855-4087-9dde-c522f0632024.kallisto.abundance.tsv.gz"
    }
  ],
  "entry": [
    {
      "fullUrl": "https://include-api-fhir-service.includedcc.org/DocumentReference/317218",
      "resource": {
        "resourceType": "DocumentReference",
        "id": "317218",
        "meta": {
          "versionId": "2",
          "lastUpdated": "2022-06-27T20:13:06.978+00:00",
          "source": "#09XK9onJ1OBmDYxw",
          "profile": [
            "https://ncpi-fhir.github.io/ncpi-fhir-ig/StructureDefinition/ncpi-drs-document-reference"
          ],
          "tag": [
            {
              "system": "https://include.org/htp/fhir/researchstudy",
              "code": "HTP"
            }
          ]
        },
        "identifier": [
          {
            "use": "official",
            "system": "https://include.org/htp/fhir/documentreference",
            "value": "HTP.0012022d-c855-4087-9dde-c522f0632024.kallisto.abundance.tsv.gz"
          }
        ],
        "status": "current",
        "docStatus": "final",
        "type": {
          "coding": [
            {
              "system": "https://includedcc.org/fhir/code-systems/data_types",
              "version": "v1",
              "code": "Gene-Expression-Quantifications",
              "display": "Gene Expression Quantifications"
            }
          ],
          "text": "Gene Expression"
        },
        "category": [
          {
            "coding": [
              {
                "system": "https://includedcc.org/fhir/code-systems/experimental_strategies",
                "version": "v1",
                "code": "RNA-Seq",
                "display": "RNA-Seq"
              }
            ],
            "text": "RNA-Seq"
          },
          {
            "coding": [
              {
                "system": "https://includedcc.org/fhir/code-systems/data_categories",
                "version": "v1",
                "code": "Transcriptomic",
                "display": "Transcriptomic"
              }
            ],
            "text": "Transcriptomic"
          }
        ],
        "subject": {
          "reference": "Patient/4941"
        },
        "securityLabel": [
          {
            "coding": [
              {
                "system": "https://includedcc.org/fhir/code-systems/data_access_types",
                "version": "v1",
                "code": "registered",
                "display": "Registered"
              }
            ]
          },
          {
            "text": "*"
          }
        ],
        "content": [
          {
            "attachment": {
              "extension": [
                {
                  "url": "https://nih-ncpi.github.io/ncpi-fhir-ig/StructureDefinition/file-size",
                  "valueDecimal": 2743960
                },
                {
                  "url": "https://nih-ncpi.github.io/ncpi-fhir-ig/StructureDefinition/hashes",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "display": "md5"
                      }
                    ],
                    "text": "69b98f149df72d8de23a6a1333a43515"
                  }
                }
              ],
              "url": "drs://data.kidsfirstdrc.org/733f0956-dac4-4ad9-b787-4e186c6530b0",
              "title": "0012022d-c855-4087-9dde-c522f0632024.kallisto.abundance.tsv.gz"
            },
            "format": {
              "display": "tsv"
            }
          }
        ],
        "context": {
          "related": [
            {
              "reference": "Specimen/297344"
            }
          ]
        }
      },
      "search": {
        "mode": "match"
      }
    }
  ]
}
```


entry --> `subject` gives me the patient

There could be an option to reverse chanin, but it does not work nicely, so the idea is:

Search for condition == `MONDO:000860` and verification-status-confirmed and subject with the Patient Id

https://include-api-fhir-service.includedcc.org/Condition?code=MONDO:0008608&verification-status=confirmed&subject=Patient/4927

if nothing found, we get search list equal to zero

```
// 20220714114620
// https://include-api-fhir-service.includedcc.org/Condition?code=MONDO%3A0008608&subject=Patient%2F4927&verification-status=confirmed&_format=json

{
  "resourceType": "Bundle",
  "id": "2811c99d-d2f8-488c-9ac9-3d605180e0c9",
  "meta": {
    "lastUpdated": "2022-07-14T09:46:20.427+00:00"
  },
  "type": "searchset",
  "total": 0,
  "link": [
    {
      "relation": "self",
      "url": "https://include-api-fhir-service.includedcc.org/Condition?_format=json&code=MONDO%3A0008608&subject=Patient%2F4927&verification-status=confirmed"
    }
  ]
}
```

which means we can search the `total` and if 0 set the `sample_type` to DS21

if instead the Patient has Trisomy 



instead if we have trosomy this is what we obtained:

https://include-api-fhir-service.includedcc.org/Condition?code=MONDO:0008608&verification-status=confirmed&subject=Patient/4929

```
// 20220714115105
// https://include-api-fhir-service.includedcc.org/Condition?code=MONDO%3A0008608&subject=Patient%2F4929&verification-status=confirmed&_format=json

{
  "resourceType": "Bundle",
  "id": "c5ad06d5-fc1e-4133-9270-38c1af212d28",
  "meta": {
    "lastUpdated": "2022-07-14T09:50:50.668+00:00"
  },
  "type": "searchset",
  "total": 1,
  "link": [
    {
      "relation": "self",
      "url": "https://include-api-fhir-service.includedcc.org/Condition?_format=json&code=MONDO%3A0008608&subject=Patient%2F4929&verification-status=confirmed"
    }
  ],
  "entry": [
    {
      "fullUrl": "https://include-api-fhir-service.includedcc.org/Condition/9089",
      "resource": {
        "resourceType": "Condition",
        "id": "9089",
        "meta": {
          "versionId": "1",
          "lastUpdated": "2022-03-11T01:36:57.396+00:00",
          "source": "#DFc1zpVt8Cb0oeZd",
          "tag": [
            {
              "system": "https://include.org/htp/fhir/researchstudy",
              "code": "HTP"
            }
          ]
        },
        "identifier": [
          {
            "use": "official",
            "system": "https://include.org/htp/fhir/condition",
            "value": "HTP0005.MONDO:0008608"
          }
        ],
        "verificationStatus": {
          "coding": [
            {
              "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
              "version": "v1",
              "code": "confirmed",
              "display": "Confirmed"
            }
          ]
        },
        "category": [
          {
            "coding": [
              {
                "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                "code": "encounter-diagnosis",
                "display": "Encounter Diagnosis"
              }
            ]
          }
        ],
        "code": {
          "coding": [
            {
              "system": "http://purl.obolibrary.org/obo/mondo.owl",
              "version": "v1",
              "code": "MONDO:0008608",
              "display": "Down Syndrome"
            },
            {
              "system": "https://nih-ncpi.github.io/ncpi-fhir-ig/data-dictionary/HTP/ds_condition",
              "code": "OfficialDSDiagnosis",
              "display": "Typically self/parent report."
            }
          ],
          "text": "Complete trisomy 21"
        },
        "subject": {
          "reference": "Patient/4929"
        }
      },
      "search": {
        "mode": "match"
      }
    }
  ]
}
```

if total is instead 1, we can set it to T21
