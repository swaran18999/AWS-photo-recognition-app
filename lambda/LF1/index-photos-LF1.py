import json
import logging
import boto3
from pip._vendor import requests
import base64

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.debug("Function invoked" + str(event) + str(context))
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    created_timestamp = event['Records'][0]['eventTime']
    
    logger.debug("---------------")
    logger.debug(str(bucket_name))
    logger.debug(str(object_key))
    logger.debug(str(created_timestamp))
    logger.debug("---------------")
    
    s3_client = boto3.client('s3')
    rekognition_client = boto3.client('rekognition')
    
    es_user="swaran18999"
    es_password="Mdmp@321"
    es_url="https://search-assignment3-photos-xbtyyd4nhakuunlm6r4gvmpuby.aos.us-east-1.on.aws"
    
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    
    logger.debug("+++++++++++++++++")
    logger.debug(response)
    logger.debug("+++++++++++++++++")
    
    base64_image=response['Body'].read()
    
    logger.debug(base64_image)
    logger.debug(json.loads(base64_image))
    
    base64_image=json.loads(base64_image)['body-json']

    decoded_image=base64.b64decode(base64_image)
    
    labels = rekognition_client.detect_labels(Image={'Bytes':decoded_image}, MaxLabels=5)
    
    logger.debug("################")
    logger.debug(str(labels))
    logger.debug("################")
    
    metadata_response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
    custom_labels = metadata_response.get('Metadata', {}).get('customlabels', '').split(',')
    
    detected_labels = [label['Name'] for label in labels['Labels']]
    
    logger.debug("||||||||||||||||||||||||||")
    logger.debug(metadata_response.get('Metadata'))
    logger.debug(custom_labels)
    logger.debug("||||||||||||||||||||||||||")
    
    if custom_labels:
        detected_labels.extend(custom_labels)
    
    logger.debug("********************")
    logger.debug(detected_labels)
    logger.debug("********************")
    
    esObject = {
        "objectKey": object_key,
        "bucket": bucket_name,
        "createdTimestamp": created_timestamp,
        "labels": detected_labels
    }
    
    logger.debug("++++++++++++++++++")
    logger.debug(str(esObject))
    logger.debug("++++++++++++++++++")
    
    url = f"{es_url}/{bucket_name}/_doc/{object_key}"
    es_response = requests.post(url, data=json.dumps(esObject), auth=(es_user, es_password), headers={"Content-Type": "application/json"})
    
    print(es_response)
    
    # TODO implement
    return {
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT',
        },
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
