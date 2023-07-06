import boto3
import json
import os

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    
    s3_client = boto3.client('s3')
    
    # 署名付きURLを取得
    get_url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': 'test_pdf.pdf'},
        ExpiresIn=600,
        HttpMethod='GET'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                'get_url': get_url,
            }
        )
    }