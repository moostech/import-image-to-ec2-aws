##Caution! This is a community script, intended for Nuage VNS PoCs and Labs. It is not meant to be used in production. 

### Import your NSG raw Image from S3 to your Amazon EC2 account

Hello there. Are you bored from manually importing the RAW VM image from your S3 to your Amazon EC2? if yes, then don't worry, I've created a python script that automates this process for you.

Here is the sccript details:
1. Verifies AWS is installed on the running machine
2. Configures aws configure command
3. Creates a trusted policy to be able to perform certain AWS operation
4. Creates a role named vmimport and give VM Import/Export access to it 
5. Creates a role policy to be able to perform certain AWS operation
6. Attaches the policy to the role 
7. Creates container file, which contains information about the image
8. Executes the role policy
9. Removes the temp files (trust-policy.json, role-policy.json, containers.json)
10. Check the status of loading the AMI image to your EC2. 

Prepare your enviroment:

Before you run the script, you should have Python, pexpect, and AWS CLI installed. If pexpect and AWS cli are not installed, just type:
- pip install pexpect
- pip install --upgrade --user awscli

### Quick Start

To use the script, type the script name and pass the aws parameters. 

Mandatory parameters are:
* access_key &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Enter your AWS Access Key (i.e., BKIAIB6QLXA536P2U4BQ)
* secret_key &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Enter your AWS Secret Key (i.e., oJdKhwd204uJgP0+2v96TDV6rs)
* region_name &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Enter your AWS S3 Region (i.e., us-west-2)
* nsg_filename &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Enter your NSG file name (i.e., Nuage-NSG-4.0.7-129-AWS.raw)
* bucket_name &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Enter your AWS S3 Bucket Name (i.e., nsgami)

>Note: For AWS root account credentials, you get credentials, such as access keys or key pairs, from the Security Credentials page in the AWS Management Console. For more information, please go to AWS webpage: http://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html


#### Here is an example of how to run it:

*python import_ami_to_ec2.py <access_key> <secret_key> <region_name> <nsg_filename> <bucket_name>*

```
python import_ami_to_ec2.py BKIAIB6QLXA536P2U4BQ oJdKhwd204uJ96TDV6rs us-west-2 Nuage-NSG-4.0.7-129-AWS.raw nsgami
```

