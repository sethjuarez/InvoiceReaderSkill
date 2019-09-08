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
        try:
            # get pdf form
            pdf = requests.get(f'{record["data"]["formUrl"]}{record["data"]["formSasToken"]}')

            # make Form Recognizer API request
            logging.info(f'CogSvc Form Request: {uri}')
            response = requests.post(uri, data=pdf, headers={ 
                'Ocp-Apim-Subscription-Key': formsRecognizerKey,
                'Content-Type': 'application/pdf' })

            records['values'].append({
                'recordId': record["recordId"],
                'data': {
                    'formUrl': record["data"]["formUrl"],
                    'invoice': convert(response.json()),
                    'error': ''
                }
            })
        except:
            _, error, _ = sys.exc_info()
            records['values'].append({
                'recordId': record["recordId"],
                'data': {
                    'formUrl': record["data"]["formUrl"],
                    'invoice': { },
                    'error': str(error)
                }
            })

    return func.HttpResponse(body=json.dumps(records), 
                             headers={ 'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*" })
