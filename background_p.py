import json
import time
import boto3
from decimal import * 
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    print('event:')
    print(event)
    #while(1):
    print('current time')
    current_time=int(time.time())
    print(current_time)
    
    dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
    table = dynamodb.Table('game_history')
    
    response = table.scan(
    ProjectionExpression = 'username,#c',ExpressionAttributeNames = {'#c': 'timestamp'}
    )
        
    records = []

    for i in response['Items']:
        records.append(i)

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression='username,timestamp',
            ExclusiveStartKey=response['LastEvaluatedKey']
            )

        for i in response['Items']:
                records.append(i)
                
    for i in range(len(records)):
            
        print('username:')
        input_name = records[i].get('username')
        print(input_name)
            
        print('timestamp:')
        input_time = records[i].get('timestamp')
        print(input_time)
            
        ###########################check if the item is longer than 1 hours ago
        if(current_time-input_time>1*3600):
            print('input time is too long ago, deleting it.')
            response = table.delete_item(Key = {'username':input_name,'timestamp':input_time } )      
        else:
            print('input time is good.')
        
    ###periodically check every hour
    #time.sleep(3600)
    
    
    
    
    
    




    
    '''
    return response

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    '''
