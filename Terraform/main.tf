resource "aws_cloudwatch_event_rule" "instance_launched" {
  name        = "InstanceLaunched"
  description = "When an instance is launched in this account in any region this fires."

  event_pattern = jsonencode({
    "source" : ["aws.ec2"],
    "detail-type" : ["AWS API Call via CloudTrail"],
    "detail" : {
      "eventSource" : ["ec2.amazonaws.com"],
      "eventName" : ["RunInstances"]
    }
  })
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.instance_launched.name
  target_id = "NotifyNewInstanceLaunched"
  arn       = "arn:aws:lambda:us-east-1:698588432660:function:NotifyNewInstanceLaunched"
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "NotifyNewInstanceLaunchedIAMRole"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# Attach AWS-managed policy for Lambda basic execution
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Inline policy for SES permissions
resource "aws_iam_role_policy" "lambda_ses_permissions" {
  name = "lambda_ses_permissions"
  role = aws_iam_role.iam_for_lambda.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ses:SendEmail"
        ]
        Resource = "*"
      }
    ]
  })
}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "../LambdaCode/lambda_function.py"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_function" "new_instance_alert_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "lambda_function_payload.zip"
  function_name = "NotifyNewInstanceLaunched"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.lambda_handler"

  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.13"

}
