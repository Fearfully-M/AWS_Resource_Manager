# AWS Resource Manager

A Python script that interacts with your AWS account using boto3. Lists S3 buckets and their sizes, uploads files programmatically, checks EC2 instance status, and generates a summary report of your cloud resources

## Overview

**AWS Resource Manager** is a Python-based command-line utility built using the `boto3` library. It prints out a separate file as a JSON report that lists S3 buckets and their sizes. In this JSON report is also the EC2 instance type status (i.e t2 or t3 micro), the instance Id, and lastly whether the instance is currently running or has stopped.  

The resource manager usage is via the command line. It can be run with no commands and defaults to the user's AWS credentials and will report the JSON file to a separate file within the same directory. Optionally the user can also type in the file path directory to a file along with the bucket name to upload a file of their choice to the S3 bucket. 

The project also demonstrates optional CLI arguments, basic file-system error handling, AWS services, and navigation of complex data structures

## Features

* **Resource Tracking**

  * Tracks S3 Bucket Names as well as their respective size
  * Tracks EC2 instance IDs, instance type and current operation status (running or stopped).
  * Allows user to upload custom file of their own to their S3 Bucket

* **CLI Handling**

  * Operates cleanly in the CLI with no arguments
  * Optional arguments only necessary for uploading files to an S3 bucket

* **Clean JSON printout**

  * Prints S3 bucket name and size and EC2 instance ID, instance type, and operational status to current directory as a JSON file

* **Least Privilege Principles**

  * Uses least privilege design principles by introducing the least permissions to the IAM user while still following the project guidelines. So, no SSH keys, no backdoor, and no root access.

  Here is a table of the permissions for each AWS service:

| AWS Service | Permissions
| -------- | --------: 
| EC2     |     Describe Instances
| S3   |     PutObject, ListBucket, ListAllMyBuckets
 

* **No User Credential Handling**

  * Prompts user with an error if they have forgotten to run 'aws configure' before using the AWS Resource Manager

## How It Works

The resource manager works as follows (assuming proper credentials)

1. run the command: python main.py
2. Outputs the users S3 buckets and EC2 instances in a JSON in the working directory
3. OR Run: python [filename] [bucketname] to upload a file to the bucket

## Tech Stack

* **Python 3.13.5**
* **[boto3](https://pypi.org/project/boto3/)** — AWS SDK used to communicate with S3 and EC2 APIs
* **`AWS Account`** — for EC2 instances and S3 Buckets
* **`AWS CLI Installed`** — to run valid AWS credentials
* **`IAM User`** — with the following permissions:
EC2: Describe Instances 
S3: PutObject, ListBucket, and ListAllMyBuckets
* **`datetime`** — JSON file timestamp generation

## Project Structure

```text
AWS_Resource_Manager/
├── main.py
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

Make sure Python 3.13.5 or a compatible Python 3 version is installed.

Verify your Python installation:

```bash
python3 --version
```
### Install AWS

#### Option 1: Official AWS Installer

```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

#### Option 2 Homebrew (if using MacOS)
```bash
brew install awscli
```

Then check if it worked with

```bash
aws --version
```

Continue the configuration with the following command:

```bash
aws configure
```

which will prompt for the following 4 things:

1. AWS Access Key ID
2. AWS Secret Access Key
3. Default region name 
4. Default output format

*note* remember to never disclose your credentials 

### Installation

Clone the repository:

```bash
git clone https://github.com/Fearfully-M/AWS_Resource_Manager
```

Navigate into the project directory:

```bash
cd AWS_Resource_Manager
```

Install the required dependency:

```bash
pip3 install -r requirements.txt
```

## Usage

Start the AWS Resource Manager with:

```bash
python3 main.py
```

*This will create a JSON in the current directory with the above EC2 metadata and the list of S3 bucket names*

For uploading a file to a S3 bucket:

```bash
python3 main.py [pathToFileName] [bucketname]
```

*This simply uploads the selected file to the S3 bucket*

## Error Handling

The resource manager handles error handling for boto3 NoCredentialsError in case the user does not configure their aws credentials

The resource manager handles four case decisions for the CLI input. 

1) No arguments - run manager normally and output JSON file
2) Filename exists but no bucket name - report to user correct usage
3) Filename does not exist but there is a bucket name - report to user correct usage
4) Filename exists and bucketname exists - upload the filename to the S3 bucket as prompted.

*Note* If the user does scenario 1 or 4, which are both correct usage, but credentials are not configured the program will remind the user to go and configure their AWS credentials

### Least Privilege Design

Incorporates least privilege design by only allowing authorized IAM user groups to use the only required permissions for EC2 (DescribeInstances) and S3 (PutObject, ListAllMyBuckets, and ListBucket)

### AWS IAM JSON Policy - Least Privilege Design

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::resource-manager-kstevens-82126",
                "arn:aws:s3:::resource-manager-kstevens-82126/*"
            ]
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": [
                "s3:ListAllMyBuckets"
            ],
            "Resource": "*"
        }
    ]
}
```

## Future Enhancements

The current implementation intentionally keeps the project lightweight. Possible future improvements include:

### CSV and/or TXT Output

Replace or supplement the current JSON output system with CSV or TXT output.

This would support many different formats and would help make it easier for a user to more easily visualize their instance and bucket data or more quickly plug information into other software by having it properly formatted. 

### Testing of Multi-Bucket and Multi-Instance Support

The current iteration of this project has been built in mind and seems to have valid code for support multiple EC2 instances as well as multiple S3 buckets but neither of these have been tested. 

### Permission and Credential Distinction

As of now the project only recognizes as a binary 'yes' or 'no' if AWS is properly configured and gives a blanket statement to tell the user to configure AWS. This could be improved upon by adding more error messages such as 'AccessDenied' to let the user know that perhaps they do indeed have AWS properly configured but their IAM user group has the wrong permissions enabled to use the AWS Resource Manager


## Project Goals

This project was built as a practical exercise to expand current Python skills as well as introducing myself to the AWS ecosystem, the concepts of EC2 and S3, and for a first introduction cloud computing and policy design with a real tangible project

The primary goals were to practice:

* Communicating with AWS API
* Introduction to IAM
* Introduction to EC2, S3, and AWS
* Navigating more complex data structures
* Introduction to and using JSON
* Learning about AWS ecosystem and billing practices
* Working with third-party Python libraries
* Improve abilities to make a more advanced CLI experience

## License MIT

Built as a portfolio project to demonstrate practical use of the boto3 Python Library and learning about the AWS ecosystem.
