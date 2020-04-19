from datetime import datetime
import boto3

client = boto3.client('cloudwatch', 'us-west-2')

SENTINEL = "Error"


def handler(event, context):
    record = event['Records'][0]['Sns']
    topic = record['TopicArn']
    message = record['Message']
    subject = record['Subject']

    print("Topic: %s" % topic)
    print("Subject: %s" % subject)
    print("Message: %s" % message)

    if SENTINEL in message or SENTINEL in subject:
        send_cloudwatch_metric(topic)
        return "KO"

    return "OK"


def send_cloudwatch_metric(topic, value=1.0):
    print("Found error, logging to CloudWatch!")
    client.put_metric_data(
        Namespace='SNS-Lab',
        MetricData=[{
            'MetricName': 'ErrorNotification',
            'Dimensions': [
                {
                    "Name": "Topic",
                    "Value": topic,
                }
            ],
            'Timestamp': datetime.utcnow(),
            'Value': value,
        }],
    )
