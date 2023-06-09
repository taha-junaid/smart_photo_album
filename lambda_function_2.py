import json
import math
import dateutil.parser
import datetime
import time
import os
import logging
import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
headers = { "Content-Type": "application/json" }
host = "https://search-pictures-t6qyfsrwuavky5fac4hs4wmrpq.us-east-1.es.amazonaws.com/newpictures/0"
region = 'us-east-1'
lex = boto3.client('lex-runtime', region_name=region)

def lambda_handler(event, context):
    q1 = event['q']
    # print(q1)
    
    #if(q1 == "searchAudio" ):
        #q1 = convert_speechtotext()
        
    #print("q1:", q1 )
    
    #q1 = "I want to see pictures of Cat and Dog"
    
    # q1 = event['queryStringParameters']['q']
    
    print ('query isssss : ', q1)
    
    response = lex.post_text(
        botName='LexTwo',                 
        botAlias ='LexTest',
        userId = "lf2-assignment-2",           
        inputText=q1
    )
    
    print("lex-respone", response)
    
    labels = []
    
    if 'slots' not in response:
        print("No photo collection for query {}".format(q1))
        
    else:
        
        print ("slot: ",response['slots'])
        
        slot_val = response['slots']
        
        for key,value in slot_val.items():
            
            if value!=None:
                labels.append(value)
                
    #return labels
    
    print("labels", labels)
    
    if len(labels) == 0:
        return
    
    else:
        resp = get_photo_path(labels)
        
 
    return resp
    #return {
        #'statusCode':200,
        
        #'body': {
        
            #'imagePaths':img_paths,
            #'userQuery':q1,
            #'labels': labels,
        #},
        
        #'headers':{
            #'Access-Control-Allow-Origin': '*'
        #}
        
    #}
    

def get_photo_path(labels):
    
    img_paths = []
    
    unique_labels = [] 
    
    for x in labels: 
        if x not in unique_labels: 
            unique_labels.append(x)
            
    labels = unique_labels
    
    # print("inside get photo path", labels)
    
    for i in labels:
        
        path = host + '/_search?q=labels:'+i
        
        # print(path)
        
        response = requests.get(path, headers=headers, auth=('Harish2023', 'Winwin2023$'))
        
        # print("response from ES", response)
        
        dict1 =  json.loads(response.text)
        
        # print(dict1)
        
        hits_count = dict1['hits']['total']['value']
        
        # print ("DICT : ", dict1)
        
        for k in range(0, hits_count):
            
            #img_obj = dict1["hits"]["hits"]
            
            img_bucket = dict1["hits"]["hits"][k]["_source"]["bucket"]
            
            # print("img_bucket", img_bucket)
            
            img_name = dict1["hits"]["hits"][k]["_source"]["objectKey"]
            
            # print("img_name", img_name)
            
            #img_link = 'https://s3.amazonaws.com/' + str(img_bucket) + '/' + str(img_name)
            
            img_link =  'https://' + str(img_bucket) + '.s3.amazonaws.com/' + str(img_name)
            # print (img_link)
            
            img_paths.append(img_link)
         
    print("imgpath linkssssss") 
    
    print (img_paths)
    
    print("total images")
    
    print(len(img_paths))
    return {'statusCode':200,'data':img_paths}
    
# def convert_speechtotext():
#     # return "blossom"
#     transcribe = boto3.client('transcribe')
   
#     job_name = datetime.datetime.now().strftime("%m-%d-%y-%H-%M%S")
#     job_uri = "https://awstranscribe-recordings.s3.amazonaws.com/Recording.wav"
#     storage_uri = "awstranscribe-output"

#     s3 = boto3.client('s3')
#     transcribe.start_transcription_job(
#         TranscriptionJobName=job_name,
#         Media={'MediaFileUri': job_uri},
#         MediaFormat='wav',
#         LanguageCode='en-US',
#         OutputBucketName=storage_uri
#     )

#     while True:
#         status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
#         if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
#             break
#         print("Not ready yet...")   
#         time.sleep(5)
    
#     print("Transcript URL: ", status)
# #     transcriptURL = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
# # 	trans_text = requests.get(transcriptURL).json()
   
#     job_name = str(job_name) + '.json'
#     print (job_name)
#     obj = s3.get_object(Bucket="awstranscribe-output", Key=job_name)
#     print ("Object : ", obj)
#     body = json.loads(obj['Body'].read().decode('utf-8'))
#     print ("Body :", body)
   
    
#     return body["results"]["transcripts"][0]["transcript"]
