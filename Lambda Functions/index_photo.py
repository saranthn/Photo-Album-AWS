import json
import boto3
from datetime import datetime
import time
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

region = 'us-east-1'
service = 'es'

credential = boto3.Session(aws_access_key_id="",
                          aws_secret_access_key="", 
                          region_name="us-east-1").get_credentials()
auth = AWS4Auth(credential.access_key, credential.secret_key, region, service)

esEndPoint = 'search-photos-6try5ru74kcnc5vx4duzcyhwbq.us-east-1.es.amazonaws.com'

es = Elasticsearch(
    hosts = [{'host': esEndPoint, 'port': 443}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

def lambda_handler(event, context):
    # TODO implement
    print(event)
    
    photo_name = event['Records'][0]['s3']['object']['key']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    
    result = detect_labels(photo_name, bucket_name)
    insert_index(result, photo_name)

    print("Success")
    
    return result

def detect_labels(photo, bucket):

    client=boto3.client('rekognition', region_name='us-east-1')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10)

    print('Detected labels for ' + photo) 
    
    labels = []
    
    for label in response['Labels']:
        labels.append(label['Name'])
    
    custom_labels = get_custom_labels(photo, bucket)
    
    for element in custom_labels:
        if element not in labels:
            labels.append(element)
            
    print(labels)
    
    result = {
        'objectKey': photo,
        'bucket': bucket,
        'createdTimestamp': datetime.now().strftime('%Y-%d-%mT%H:%M:%S'),
        'labels': labels
    }
    
    return result
    
def get_custom_labels(photo, bucket):
    s3 = boto3.client('s3')
    response = s3.head_object(Bucket=bucket, Key=photo)
    print(response['Metadata']['customlabels'].split(','))
    return response['Metadata']['customlabels'].split(',')
    
    
def insert_index(result, photo_name):
    
    es.index(index="photos", doc_type="photo", id=photo_name, body=result)
    
    return
    pass
