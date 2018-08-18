import boto3
import io
import zipfile
import mimetypes

def lambda_handler(event, context):
    # set AWS_PROFILE=aws_personal
    s3=boto3.resource('s3')
    codebuild_buccket = s3.Bucket('portfolio.codebuild.pipeline')
    portfolio_bucket = s3.Bucket('agni-portfolio')
    portfolio_zip = io.BytesIO()
    codebuild_file=codebuild_buccket.download_fileobj('portfoliobuild.zip', portfolio_zip)
    with zipfile.ZipFile(portfolio_zip) as myzip:
        for name in myzip.namelist():
            obj = myzip.open(name)
            portfolio_bucket.upload_fileobj(obj,name,
            ExtraArgs={'ContentType': mimetypes.guess_type(name)[0]})
            portfolio_bucket.Object(name).Acl().put(ACL='public-read')

    return 'Hello from Lambda'
