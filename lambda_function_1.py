import logging
import base64
import json
import boto3
import os
import requests
import datetime
from io import BytesIO

def lambda_handler(event, context):
    # print(event)
    
    Trigger_info = event['Records'][0]['s3']

    BucketName = Trigger_info['bucket']['name']
    KeyName = Trigger_info['object']['key']
    # BucketName = 'pictures-assignment2'
    # KeyName = '1679696031006cat4.jpeg'
    # print("bucketname",BucketName )
    # print("keyname",KeyName )
    
    s3 = boto3.client('s3')
    s3obj = s3.get_object(Bucket=BucketName, Key=KeyName)

    customlabels = s3obj['ResponseMetadata']['HTTPHeaders']['x-amz-meta-customlabels'].split(',')

    base64_image_binary = s3obj['Body'].read() #this contains data:image/jpeg;base64, 
    base64_image_string_only_data = base64_image_binary.decode('utf-8').split(',')[1]
    image_bytes = bytes(base64.b64decode(base64_image_string_only_data))
    
    client = boto3.client('rekognition')
    rekognitionImageObj = {'Bytes': image_bytes}
    resp = client.detect_labels(Image=rekognitionImageObj)

    timestamp =str(datetime.datetime.now())
    
    labels = customlabels

    for i in range(len(resp['Labels'])):
        labels.append(resp['Labels'][i]['Name'].lower())
    
    indexObj = {"objectKey": KeyName,"bucket":BucketName,"createdTimestamp":timestamp,"labels":labels}
    
    url = "https://search-pictures-t6qyfsrwuavky5fac4hs4wmrpq.us-east-1.es.amazonaws.com/newpictures/0"
    
    #url = "https://search-photoboot-53tyon3nsbikh7e7qkyc26ivzm.us-west-2.es.amazonaws.com/photos/_doc"
   
    headers = {"Content-Type": "application/json"}
    
    #r = requests.post(url, data=json.dumps(indexObj).encode("utf-8"), headers=headers)
    
    r = requests.post(url, data=json.dumps(indexObj).encode("utf-8"), headers=headers,auth=('Harish2023', 'Winwin2023$'))
    
    # print(r.text)
    
    return {
        'statusCode': 200,
        'body': json.dumps(indexObj)
    }
