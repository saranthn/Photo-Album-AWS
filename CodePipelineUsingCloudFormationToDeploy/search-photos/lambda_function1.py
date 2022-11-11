import json
import boto3
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
    
    query = event['q']
    print("event: ",event)
    
    client = boto3.client('lexv2-runtime')
    
    response = client.recognize_text(
        botId='LGYZQ7MOBV',
        botAliasId='TSTALIASID',
        localeId='en_US',
        sessionId="test_session",
        text=query)
        
    # keyword1 = response['sessionState']['intent']['slots']['keyword1']['value']['originalValue']
    # keyword2 = response['sessionState']['intent']['slots']['keyword2']['value']['originalValue']
    
    slots = response['sessionState']['intent']['slots']
    label_list = []
    
    if slots is None:
        print("No slots provided")
    else:
        for slotName in slots:
            if slots[slotName] is not None:
                print(slots[slotName]['value']['originalValue'])
                keyword = slots[slotName]['value']['originalValue']
                if keyword[-1] == 's':
                    keyword = keyword[:-1]
                label_list.append(keyword)
    
    print(label_list)
    
    search_responses = []
    for label in label_list:
        if label is not None and label != '':
            search_response = es.search({"query": {"match": {"labels": label}}})
            search_responses.append(search_response)
            
    photo_urls = []
    results = []
    for search_response in search_responses:
        if 'hits' in search_response:
            for value in search_response['hits']['hits']:
                photo_name = value['_source']['objectKey']
                photo_labels = value['_source']['labels']
                print(photo_labels)
                #photo_url = 's3://photos-st3523/' + photo_name
                photo_url = 'https://photos-st3523.s3.amazonaws.com/' + photo_name
                
                if photo_url not in photo_urls:
                    photo_urls.append(photo_url)
                    results.append({
                        "url": photo_url,
                        "labels": photo_labels
                    })
                    
                    
    body = {
        "results": results
    }

    print("Success")
    
    return body