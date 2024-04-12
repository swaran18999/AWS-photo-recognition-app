import json
import boto3
import secrets
from pip._vendor import requests
import json

import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    
    
    logger.debug("{{{{{{{{{{{{{{{{{{{{{{")
    logger.debug(json.dumps(event))
    logger.debug("{{{{{{{{{{{{{{{{{{{{{{")
    logger.debug(event["params"]["querystring"]["q"])
    # logger.debug(event["queryStringParameters"]['q'])
    logger.debug(str(context))
    logger.debug("{{{{{{{{{{{{{{{{{{{{{{")
    
    q=event["params"]["querystring"]["q"]
    
    botId='OZV74BYV9N'
    botAliasId='G1ISETT344'
    localeId='en_US'
    
    client = boto3.client('lexv2-runtime')

    response = client.recognize_text(
        botId=botId,
        botAliasId=botAliasId,
        localeId=localeId,
        sessionId="sessionId",
        text=q 
    )
    
    logger.debug("####################")
    
    q1 = ""
    q2 = ""
    
    if 'sessionState' in response and 'intent' in response['sessionState'] and 'slots' in response['sessionState']['intent']:
        if 'query1' in response['sessionState']['intent']['slots'] and response['sessionState']['intent']['slots']['query1'] is not None and 'value' in response['sessionState']['intent']['slots']['query1'] and response['sessionState']['intent']['slots']['query1']['value'] is not None:
            q1 = response['sessionState']['intent']['slots']['query1']['value']['interpretedValue']
            # logger.debug(q1)
        if 'query2' in response['sessionState']['intent']['slots'] and response['sessionState']['intent']['slots']['query2'] is not None and 'value' in response['sessionState']['intent']['slots']['query2'] and response['sessionState']['intent']['slots']['query2']['value'] is not None:
            q2 = response['sessionState']['intent']['slots']['query2']['value']['interpretedValue']
            # logger.debug(q2)

    logger.debug("####################")

    es_user="swaran18999"
    es_password="Mdmp@321"
    es_url="https://search-assignment3-photos-xbtyyd4nhakuunlm6r4gvmpuby.aos.us-east-1.on.aws"

    images = []

    if q1 is not None and q1 != "":
        logger.debug("q1 " + q1)
        response = requests.get(es_url + '/_search/?q=labels:' + q1, auth=(es_user, es_password), headers={"Content-Type": "application/json"})
        logger.debug("--------------")
        logger.debug(json.loads(response.text))
        logger.debug("--------------")
        response = json.loads(response.text)
        hits = response["hits"]["hits"]
        logger.debug(hits)
        for item in hits:
            bucket = item['_source']['bucket']
            object_key = item['_source']['objectKey']
            return_value = f"{bucket}/{object_key}"
            images.append(return_value)
    else:
        logger.debug("q1 is empty")        

    if q2 is not None and q2 != "":
        logger.debug("q2 " + q2)
        response = requests.get(es_url + '/_search/?q=labels:' + q2, auth=(es_user, es_password), headers={"Content-Type": "application/json"})
        logger.debug("--------------")
        logger.debug(json.loads(response.text))
        logger.debug("--------------")
        response = json.loads(response.text)
        hits = response["hits"]["hits"]
        logger.debug(hits)
        for item in hits:
            bucket = item['_source']['bucket']
            object_key = item['_source']['objectKey']
            return_value = f"{bucket}/{object_key}"
            images.append(return_value)
    else:
        logger.debug("q2 is empty")

    
    return {
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        },
        'statusCode': 200,
        'messages': "All good lads",
        'images': images
    }