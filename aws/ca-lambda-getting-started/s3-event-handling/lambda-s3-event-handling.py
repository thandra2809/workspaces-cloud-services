import os, zipfile, StringIO
import boto3

s3 = boto3.client('s3')


def lambda_handler(event, context):
    # read bucket and key from event data
    record = event['Records'][0]['s3']
    bucket = record['bucket']['name']
    key = record['object']['key']

    # generate new key name
    new_key = "zip/%s.zip" % os.path.basename(key)

    # read the source obj content
    body = s3.get_object(Bucket=bucket, Key=key)['Body'].read()

    # create new obj with compressed data
    s3.put_object(
        Body=compress(body, key),
        Key=new_key,
        Bucket=bucket,
    )

    return "OK"


def compress(body, key):
    data = StringIO.StringIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as f:
        f.writestr(os.path.basename(key), body)
    data.seek(0)
    return data.read()
