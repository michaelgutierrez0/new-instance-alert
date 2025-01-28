import json
import boto3

# Initialize the SES client
client = boto3.client('ses')

def pull_creator(event):
    creator = event['detail']['userIdentity']['arn']
    creator = creator.split('/')
    creator = creator[2]
    return creator

def pull_instance_type(event):
    instance_type = event['detail']['requestParameters']['instanceType']
    return instance_type

def pull_instance_id(event):
    instance_id = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']
    return instance_id

def pull_instance_name(event):
    instance_name = event['detail']['responseElements']['instancesSet']['items'][0]['tagSet']['items'][0]['value']
    return instance_name

from_email = "mgutierrez@jsr-nahq.com"
to_email_list = ["jdavidson@jsr-nahq.com", "mgutierrez@jsr-nahq.com", "icavalcante@jsr-nahq.com"]

def lambda_handler(event, context):
    print(f"For debugging purposes here is the event that came in: {event}")

    # Pull the required data from the event
    creator = pull_creator(event)
    instance_type = pull_instance_type(event)
    instance_id = pull_instance_id(event)
    instance_name = pull_instance_name(event)

    # Build the dynamic HTML content
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                margin: 20px;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
            }}
            .header {{
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .content {{
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">New Instance Launched</div>
            <div class="content">
                <p>
                    User: <strong>{creator}</strong><br>
                    Started an instance with the following details:
                </p>
                <ul>
                    <li><strong>Instance Type:</strong> {instance_type}</li>
                    <li><strong>Instance ID:</strong> {instance_id}</li>
                    <li><strong>Instance Name:</strong> {instance_name}</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

    # Send the email with dynamic HTML content
    response = client.send_email(
        Source=from_email,
        Destination={
            'ToAddresses': to_email_list
        },
        Message={
            'Subject': {
                'Data': 'New Instance Launched In Dev Account',
                'Charset': 'UTF-8'
            },
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': html_content
                }
            }
        },
        ReplyToAddresses=[
            from_email,
        ])

    return {
        'statusCode': 200,
        'body': json.dumps('Email sent successfully!')
    }
