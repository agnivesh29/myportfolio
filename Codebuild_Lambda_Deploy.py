import boto3
import io
import zipfile
import mimetypes

def lambda_handler(event, context):
    # set AWS_PROFILE=aws_personal
    s3=boto3.resource('s3')
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:ap-southeast-2:586861109696:PortfolioDeployCompleted')
    job = event.get('CodePipeline.job')
    location = {
        'bucketName': 'portfolio.codebuild.pipeline',
        'objectKey': 'portfoliobuild.zip'
    }
    if job:
        for artifact in job['data']['inputArtifacts']:
            if artifact['Name'] == 'MyAppBuild':
                location = artifact['location']['s3Location']

    print('Building portfolio from {}'.format(str(location)))
    try:
        codebuild_buccket = s3.Bucket(location['bucketName'])
        portfolio_bucket = s3.Bucket('agni-portfolio')
        portfolio_zip = io.BytesIO()
        codebuild_file=codebuild_buccket.download_fileobj(location['objectKey'], portfolio_zip)
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for name in myzip.namelist():
                obj = myzip.open(name)
                portfolio_bucket.upload_fileobj(obj,name,
                ExtraArgs={'ContentType': mimetypes.guess_type(name)[0]})
                portfolio_bucket.Object(name).Acl().put(ACL='public-read')
        topic.publish(Subject='Portfolio deployed successfully',Message='Congratulation !!! Lambda has successfully deployed the portfolio to s3')
        if job:
            code_pipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job['Id'])
    except:
        topic.publish(Subject='Code deploy failed', Message='Code deployment to S3 via Lambda failed')
        raise;

    return 'Hello from Lambda'
