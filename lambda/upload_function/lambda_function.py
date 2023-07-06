import boto3
import json
import os

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    
    s3_client = boto3.client('s3')
    
    # 署名付きURLを取得
    put_url = s3_client.generate_presigned_url(
        ClientMethod='put_object',
        Params={'Bucket': bucket_name, 'Key': 'test.pptx'},
        ExpiresIn=600,
        HttpMethod='PUT'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                'put_url': put_url,
            }
        )
    }