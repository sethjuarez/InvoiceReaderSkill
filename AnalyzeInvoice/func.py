import os
import sys
import json
import logging
import requests
import azure.functions as func
from lib.helpers import convert

formsRecognizerKey = os.environ["FormsRecognizerKey"]
formsRecognizerEndpoint = os.environ["FormsRecognizerEndpoint"]
modelId = os.environ["ModelId"]
uri = f"https://{formsRecognizerEndpoint}/formrecognizer/v1.0-preview/custom/models/{modelId}/analyze"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Invoice Skill Request: Python HTTP trigger function processed a request.')
    
    # get request body
    body = req.get_json()

    # prep return shape
    records = { 'values': [] }

    for record in body["values"]:
        recordId = record["recordId"]
        url = record["data"]["formUrl"]
        token = record["data"]["formSasToken"]

        try:
            # get pdf form
            pdf = requests.get(f"{url}{token}")

            # make Form Recognizer API request
            response = requests.post(uri, data=pdf, headers={ 
                'Ocp-Apim-Subscription-Key': formsRecognizerKey,
                'Content-Type': 'application/pdf' })

            logging.info(type(response.json()))

            records['values'].append({
                'recordId': recordId,
                'data': {
                    'formUrl': url,
                    'invoice': convert(response.json()),
                    'error': ""
                }
            })

        except:
            _, error, _ = sys.exc_info()
            records['values'].append({
                'recordId': recordId,
                'data': {
                    'formUrl': url,
                    'invoice': { },
                    'error': str(error)
                }
            })

    return func.HttpResponse(body=json.dumps(records), 
                             headers={ 'Content-Type': 'application/json' })
