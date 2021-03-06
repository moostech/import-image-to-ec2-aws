##Caution! This is a community script, intended for Nuage VNS PoCs and Labs. It is not meant to be used in production. 

### Import your OVA/VMDK/RAW Image from S3 to your Amazon EC2 account

Hello there. Are you bored from manually importing the OVA/VMDK/RAW VM image from your S3 to your Amazon EC2? if yes, then don't worry, I've created a python script that automates this process for you.

### Here is the script details:
1. Verifies AWS is installed on the running machine
2. Configures "aws configure" command to connect to your AWS account
3. Creates a trusted policy to be able to perform certain AWS operation
4. Creates a role named vmimport and give VM Import/Export access to it 
5. Attaches the policy to the role 
6. Creates a file, which contains information about the image
7. Executes the role policy
8. Checks the status of loading the OVA/VMDK/AMI image to your EC2. 

### Prepare your enviroment:

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
python import_ami_to_ec2.py BKIAIB6QLXA536PcU4BQ oJdKhwd2cccJ96TDV6rs us-west-2 Nuage-NSG-4.0.7-129-AWS.raw nsgami
```
*python import_ova_to_ami.py <access_key> <secret_key> <region_name> <vm_filename> <bucket_name>*
```
python import_ova_to_ami.py AKIAIB6QLXA53CC2U4BQ oJdKhwdcc4uJgD9sENCCjlCCCdHP0+2vCCTDVCCs us-west-2 linux_vm.ova Mybucket
```



