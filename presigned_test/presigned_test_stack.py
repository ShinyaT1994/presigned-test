import os

from aws_cdk import (
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_s3 as s3,
)
from constructs import Construct

class PresignedTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Test用のS3Bucketを作成
        bucket = s3.Bucket(self, 'TestBucket')
        
        # /upload ファイルアップロード用にS3の署名付きURLを取得する関数
        upload_function = lambda_.Function(
            self,
            'UploadFunction',
            code=lambda_.Code.from_asset(
                os.path.join('lambda', 'upload_function')
            ),
            handler='lambda_function.lambda_handler',
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment={
                'BUCKET_NAME': bucket.bucket_name,
            },
            function_name='upload-bucket',
        )
        
        bucket.grant_write(upload_function)
        
        # /download ファイルダウンロード用にS3の署名付きURLを取得する関数
        download_function = lambda_.Function(
            self,
            'DownloadFunction',
            code=lambda_.Code.from_asset(
                os.path.join('lambda', 'download_function')
            ),
            handler='lambda_function.lambda_handler',
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment={
                'BUCKET_NAME': bucket.bucket_name,
            },
            function_name='download-bucket',
        )
        
        bucket.grant_read(download_function)
        
        # APIを作成
        rest_api = apigateway.RestApi(
            self,
            'RestApi',
            deploy=True,
            deploy_options=apigateway.StageOptions(stage_name='test'),
            rest_api_name='presigned-test-api',
        )
        
        # lambda integrationを作成
        upload_integration = apigateway.LambdaIntegration(
            handler=upload_function,
            integration_responses=[
                apigateway.IntegrationResponse(status_code='200')
            ],
        )
        download_integration = apigateway.LambdaIntegration(
            handler=download_function,
            integration_responses=[
                apigateway.IntegrationResponse(status_code='200')
            ],
        )
        
        # リソースを追加
        upload_resource = rest_api.root.add_resource(path_part='upload')
        download_resource = rest_api.root.add_resource(path_part='download')
        
        # Methodを追加
        upload_resource.add_method(
            http_method='GET',
            integration=upload_integration,
            method_responses=[
                apigateway.MethodResponse(status_code='200')
            ],
        )
        download_resource.add_method(
            http_method='GET',
            integration=download_integration,
            method_responses=[
                apigateway.MethodResponse(status_code='200')
            ],
        )

