# New Instance Alert

This project sets up an AWS Lambda function that sends an email notification whenever a new EC2 instance is launched in your AWS account. The notification includes details about the instance such as the instance type, instance ID, and instance name.

## Project Structure

- **LambdaCode/lambda_function.py**: Contains the AWS Lambda function code that sends the email notification.
- **Terraform/**: Contains the Terraform configuration files to set up the necessary AWS resources.
- **.gitignore**: Specifies files and directories to be ignored by Git.
- **LICENSE**: The license for this project.
- **README.md**: This file.

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) installed on your local machine.
- AWS CLI configured with appropriate permissions to create IAM roles, Lambda functions, and CloudWatch events.
- An SES verified email address to send notifications from.

## Setup

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Navigate to the Terraform directory:**

    ```sh
    cd Terraform
    ```

3. **Initialize Terraform:**

    ```sh
    terraform init
    ```

4. **Apply the Terraform configuration:**

    ```sh
    terraform apply
    ```

    This command will create the necessary AWS resources including the IAM role, Lambda function, and CloudWatch event rule.

## Lambda Function

The Lambda function is written in Python and is located in the [lambda_function.py](http://_vscodecontentref_/6) file. It uses the AWS SES service to send an email notification with the details of the newly launched EC2 instance.

### Environment Variables

- [from_email](http://_vscodecontentref_/7): The email address from which the notification will be sent.
- [to_email_list](http://_vscodecontentref_/8): A list of email addresses to which the notification will be sent.

## Terraform Configuration

The Terraform configuration files are located in the [Terraform](http://_vscodecontentref_/9) directory. The main configuration is in the [main.tf](http://_vscodecontentref_/10) file, which defines the AWS resources needed for this project.

### Resources

- **aws_cloudwatch_event_rule**: Triggers the Lambda function when a new EC2 instance is launched.
- **aws_cloudwatch_event_target**: Specifies the Lambda function to be triggered by the event rule.
- **aws_iam_role**: Defines the IAM role for the Lambda function.
- **aws_iam_role_policy_attachment**: Attaches the AWS-managed policy for Lambda basic execution to the IAM role.
- **aws_iam_role_policy**: Defines an inline policy for SES permissions.
- **aws_lambda_function**: Defines the Lambda function.

## License

This project is licensed under the MIT License. See the [LICENSE](http://_vscodecontentref_/11) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or inquiries, please contact Michael Gutierrez via [LinkedIn](https://www.linkedin.com/in/michael-gutierrez-se/).
