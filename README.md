# 🚀 Project: EC2 Instance Control via Lambda, S3, API Gateway & EventBridge

This project demonstrates how to **start and stop an EC2 instance** using a web-based interface hosted on S3. The backend logic is powered by **AWS Lambda functions**, triggered via **API Gateway**, and automated using **Amazon EventBridge** with a cron rule. It also involves **IAM role configuration** to manage permissions securely.

---

## 🧰 Services Used

<a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html">
  <img src="https://icon.icepanel.io/AWS/svg/Security-Identity-Compliance/IAM-Identity-Center.svg" alt="IAM Identity Center" width="80">
</a>

<a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html">
  <img src="https://icon.icepanel.io/AWS/svg/Compute/EC2.svg" alt="EC2" width="80">
</a> 

<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html" target="_blank">
  <img src="https://icon.icepanel.io/AWS/svg/Storage/Simple-Storage-Service.svg" alt="Amazon S3" width="80">
</a>

<a href="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html" target="_blank">
  <img src="https://icon.icepanel.io/AWS/svg/Compute/Lambda.svg" alt="AWS Lambda" width="80">
</a>

<a href="https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html" target="_blank">
  <img src="https://icon.icepanel.io/AWS/svg/App-Integration/API-Gateway.svg" alt="API Gateway" width="80">
</a>

<a href="https://docs.aws.amazon.com/eventbridge/latest/userguide/what-is-amazon-eventbridge.html" target="_blank">
  <img src="https://icon.icepanel.io/AWS/svg/App-Integration/EventBridge.svg" alt="EventBridge" width="80">
</a>

<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html" target="_blank">
  <img src="https://icon.icepanel.io/AWS/svg/Management-Governance/CloudWatch.svg" alt="CloudWatch" width="80">
</a>


- **IAM** - To manage permissions and access control.
- **Amazon EC2** - For launching and managing virtual servers.
- **Amazon S3** - To host the static website with Start/Stop buttons.
- **AWS Lambda** - To create functions for starting and stopping EC2 instances.
- **Amazon API Gateway** - To expose Lambda functions as HTTP endpoints.
- **Amazon EventBridge** - To automate start/stop using scheduled cron jobs.
- **Cloud Watch** - To monitor the EC2 instance status.
---

## 📝 Project Steps

### 1. ✅ IAM User Setup

Create an IAM user and assign the following permissions:

- `AmazonEC2FullAccess`
- `AmazonS3FullAccess`
- `AWSLambdaBasicExecutionRole`

![IAM Role](/Snap/IAM-role.png)

---

### 2. 🗂️ Create an S3 Bucket for Static Website Hosting
- Create Bucket
![](/Snap/s3-bucket.png)

- Enable **Static Website Hosting** on the bucket.
![](/Snap/enable-static-hosting.png)

- Upload your `index.html` with **Start** and **Stop** buttons.
![](/Snap/s3-index-page.png)

- Set appropriate **bucket policy** to allow public access (or control via CloudFront).
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::ec2-trigger-bucket-2025/*"
        }
    ]
}
```
![](/Snap/s3-permissions.png)

- The buttons should trigger the API Gateway endpoints (we’ll create them later).
![](/Snap/s3-webpage.png)
---

### 3. 💻 Create an EC2 Instance

- Launch an EC2 instance in region: `us-east-1`.
- Copy the **Instance ID** and **AMI ID** – these will be used in the Lambda code.


![](/Snap/ec2-start-event-bridge.png)

---

### 4. 🧠 Lambda Functions

Create two Lambda functions in `us-east-1`:

- `startEC2Instance`
- `stopEC2Instance`

###  Lambda Code Snippet:

startEC2Instance.py
```python
import boto3

def lambda_handler(event, context):
    print("Step1: Starting EC2 instance process")
    
    ec2 = boto3.client('ec2', region_name='<aws-region>')
    ec2.start_instances(InstanceIds=['<Instance-ID>'])

    print("Step2: EC2 instance started successfully!!")
    return {
        'statusCode': 200,
        'body': 'EC2 instance started successfully!'
    }
```
```python
import boto3

def lambda_handler(event, context):
    print("Step1: Stopping EC2 instance process")
    
    ec2 = boto3.client('ec2', region_name='<aws-region>')
    ec2.stop_instances(InstanceIds=['<Instance-ID>'])

    print("Step2: EC2 instance stopped successfully!!")
    return {
        'statusCode': 200,
        'body': 'EC2 instance stopped successfully!'
    }

```
![](/Snap/lambda-start-code.png)
![](/Snap/lambda-stop-code.png)

- Do the same for the `stop_instances` method in the stop function.
- Set **Lambda timeout** to **10 seconds**.

![](/Snap/lambda-start-timeout.png)
![](/Snap/lambda-stop-timeout.png)
---

### 5. 🌐 Configure API Gateway

- Create a **REST API** with two endpoints: `/start` and `/stop`.
- Integrate each endpoint with the corresponding Lambda function.
- Enable **CORS** so it can be called from the S3-hosted frontend.

![](/Snap/lambda-start-trigger.png)
![](/Snap/lambda-stop-trigger.png)
---

### 6. 🧪 Test from Browser

- Open your S3 website URL in a browser.
- Click **Start** or **Stop** buttons.
- They should invoke the API Gateway endpoints and control the EC2 instance.
![](/Snap/s3-webpage.png)
---

### 7. 🔁 Automate with EventBridge

Ref doc: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-scheduled-rule-pattern.html
- Create a **rule** with a **cron schedule** (e.g., every 3 minutes):

```cron
cron(0/3 * * * ? *)
```

- Set the rule to **trigger the start Lambda function**.

You can also set another rule to stop the instance after a delay if needed.

![](/Snap/evnetBridge-trigger.png)
---

## 🌟 Final Flow

1. User accesses the static site from S3.
2. Button click → API Gateway → Lambda → EC2 Action.
3. Every 3 minutes, EventBridge triggers EC2 start via Lambda.
4. Check in CloudWatch logs for Lambda and EC2 actions.
![](/Snap/s3-webpage.png)
![](/Snap/ec2-start-event-bridge.png)
![](/Snap/cloudwatch-log.png)
---

## 📌 Notes

- Ensure proper security and cleanup of unused resources to avoid costs.
- Always validate IAM roles and least-privilege access.
- Monitor Lambda and EC2 usage via **CloudWatch Logs**.

---

## References:
## **IAM role:** https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html
## **S3 web hosting:** https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html
## **Ec2 launch:** https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/tutorial-launch-my-first-ec2-instance.html
## **EventBridge cron job:** https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-scheduled-rule-pattern.html
