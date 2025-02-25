import json
import boto3
import logging
from typing import Any, Dict

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define the email addresses to send the email from
FROM_EMAIL = "mgutierrez@jsr-nahq.com"

# Define the email addresses to send the email to
TO_EMAIL_LIST = ["jdavidson@jsr-nahq.com", "mgutierrez@jsr-nahq.com", "icavalcante@jsr-nahq.com"]

# Email subject
EMAIL_SUBJECT = "New Instance Launched In Dev Account"

# Initialize the SES client
client = boto3.client('ses')

def get_event_detail(event: Dict[str, Any], keys: list, default: str = "Unknown") -> str:
    """Helper function to safely extract nested values from the event."""
    try:
        value = event
        for key in keys:
            value = value[key]
        return value
    except KeyError:
        return default

def pull_creator(event: Dict[str, Any]) -> str:
    """Extract the creator's ARN from the event."""
    return get_event_detail(event, ['detail', 'userIdentity', 'arn']).split('/')[-1]

def pull_instance_type(event: Dict[str, Any]) -> str:
    """Extract the instance type from the event."""
    return get_event_detail(event, ['detail', 'requestParameters', 'instanceType'])

def pull_instance_id(event: Dict[str, Any]) -> str:
    """Extract the instance ID from the event."""
    return get_event_detail(event, ['detail', 'responseElements', 'instancesSet', 'items', 0, 'instanceId'])

def pull_instance_name(event: Dict[str, Any]) -> str:
    """Extract the instance name from the event."""
    return get_event_detail(event, ['detail', 'responseElements', 'instancesSet', 'items', 0, 'tagSet', 'items', 0, 'value'])

def pull_iam_role(event: Dict[str, Any]) -> str:
    """Extract the IAM role from the event."""
    return get_event_detail(event, ['detail', 'responseElements', 'instancesSet', 'items', 0, 'iamInstanceProfile', 'arn']).split('/')[-1]

def create_html_content(creator: str, instance_type: str, instance_id: str, instance_name: str, instance_role: str) -> str:
    """Create the HTML content for the email."""
    return f"""
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
                    <li><strong>IAM Role:</strong> {instance_role}</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """

def send_email(html_content: str) -> bool:
    """Send the email with the given HTML content."""
    try:
        response = client.send_email(
            Source=FROM_EMAIL,
            Destination={
                'ToAddresses': TO_EMAIL_LIST
            },
            Message={
                'Subject': {
                    'Data': EMAIL_SUBJECT,
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
                FROM_EMAIL,
            ])
        logger.info(f"Email sent successfully: {response}")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda function handler."""
    logger.info(f"Received event: {json.dumps(event)}")

    # Pull the required data from the event
    creator = pull_creator(event)
    instance_type = pull_instance_type(event)
    instance_id = pull_instance_id(event)
    instance_name = pull_instance_name(event)
    instance_role = pull_iam_role(event)

    # Build the dynamic HTML content
    html_content = create_html_content(creator, instance_type, instance_id, instance_name, instance_role)

    # Send the email
    if send_email(html_content):
        return {
            'statusCode': 200,
            'body': json.dumps('Email sent successfully!')
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps('Error sending email.')
        }
