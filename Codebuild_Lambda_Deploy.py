# set AWS_PROFILE=aws_personal
import boto3
import io
import zipfile
import mimetypes

s3=boto3.resource('s3')
codebuild_buccket = s3.Bucket('portfolio.codebuild.pipeline')
portfolio_bucket = s3.Bucket('agni-portfolio')

# codebuild_file=codebuild_buccket.download_file('portfoliobuild.zip','C:/Users/AArya/Downloads/Temp/portfoliobuild.zip')

portfolio_zip = io.BytesIO()
codebuild_file=codebuild_buccket.download_fileobj('portfoliobuild.zip', portfolio_zip)
with zipfile.ZipFile(portfolio_zip) as myzip:
    for name in myzip.namelist():
        obj = myzip.open(name)
        portfolio_bucket.upload_fileobj(obj,name,
        ExtraArgs={'ContentType': mimetypes.guess_type(name)[0]})
        portfolio_bucket.Object(name).Acl().put(ACL='public-read')
