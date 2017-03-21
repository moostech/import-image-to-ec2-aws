#!/usr/bin/env python

# Created on 2017-3-13
# 
# @author: Mostafa Mostafa
# @copyright: Nokia 2017
# @version: 1.0.0
# 
# PRE-REQUISTES:
#    To run the script, you need to install pexpect and AWS-cli, just type:
#        - pip install pexpect
#        - pip install --upgrade --user awscli
#
# USAGE: 
#     python import_ami_to_ec2.py
#     CLI argument to run the script is:
#        - python import_ami_to_ec2.py <access_key> <secret_key> <region_name> <nsg_filename> <s3_bucket_name>
#        - For example: 
#          python import_ami_to_ec2.py BKIAIB6QLXA536P2U4BQ oJdKhwd204uJgD9sENd7jlFW+dHP0+2v96TDV6rs us-west-2 Nuage-NSG-4.0.7-129-AWS.raw nsgami
#
# Script Summary:
#     This script import a raw image from your S3 to your EC2.
#
# Script Details:
#     1) Verifies AWS is installed on the running machine
#     2) Configures aws configure command
#     3) Creates a trusted policy to be able to perform certain AWS operation
#     4) Creates a role named vmimport and give VM Import/Export access to it 
#     5) Creates a role policy to be able to perform certain AWS operation
#     6) Attaches the policy to the role 
#     7) Creates container file, which contains information about the image
#     8) Executes the role policy
#     9) Removes the temp files (trust-policy.json, role-policy.json, containers.json)
#     10) Check the status of loading the AMI image to your EC2. 
#

############################################# 
# Import required libraries
############################################# 
import pexpect, os, sys, time, argparse


############################################# 
# Start script
############################################# 
### start main function
def main():
    # add cli options (email, github, interval) 
    parser = argparse.ArgumentParser()
    parser.add_argument("access_key", default="", type=str,
                        help="Enter your AWS Access Key")
    parser.add_argument("secret_key", default="", type=str,
                        help="Enter your AWS Secret Key")
    parser.add_argument("region_name", default="us-west-2", type=str,
                        help="Enter your AWS S3 Region")
    parser.add_argument("nsg_filename", default="Nuage-NSG-4.0.7-129-AWS.raw", type=str,
                        help="Enter your NSG file name")
    parser.add_argument("bucket_name", default="nsgami", type=str,
                        help="Enter your AWS S3 Bucket Name")
    args = parser.parse_args()
    #print(args)

    #save cli variables
    access_key = args.access_key                   
    secret_key = args.secret_key
    region_name = args.region_name
    nsg_filename = args.nsg_filename
    bucket_name = args.bucket_name

    # check aws is installed correctly 
    print '1) Verify AWS installation'
    try:
        output = pexpect.run('aws --version')
        if not "aws-cli" in output:
            print 'ERROR: AWS is not installed in this machine. Please install AWS-CLI.'
            print '      For information regarding this procedure, refer to the current AWS official documentation at: '
            print '      http://docs.aws.amazon.com/cli/latest/userguide/installing.html#install-bundle-other-os'
            sys.exit()
    except:
        sys.exit()

    #check if enviroment variables are set correctly
    try:
        os.environ["LC_ALL"]
    except:
        #print '    - Setting enviroment variables (i.e., LC_ALL) required for running AWS CLI'
        os.environ["LC_ALL"] = "en_US.UTF-8"
        os.environ["LC_CTYPE"] = "UTF-8"
        os.environ["LANG"] = "en_US"

    #check if the bucket name exists
    try:
        output = pexpect.run('aws s3 ls')
        if not bucket_name in output:
            print 'ERROR: Bucket Name does not exist in the specified region :'+ region_name
            sys.exit()
    except:
        print 'ERROR: Bucket Name does not exist in the specified region :'+ region_name
        sys.exit()

    #check if the AMI image exists
    try:
        output = pexpect.run('aws s3 ls %s' % bucket_name)
        if not nsg_filename in output:
            print 'ERROR: AMI Image Name does not exist in the specified region :'+ bucket_name
            sys.exit()
    except:
        print 'ERROR: AMI Image Name does not exist in the specified region :'+ bucket_name
        sys.exit()
    
    print '2) Configure AWS CLI by execute aws configure'
    child = pexpect.spawn ('aws configure')
    #child.interact()
    child.expect ('AWS Access Key ID')
    child.sendline ('%s' % access_key)
    child.expect ('AWS Secret Access Key')
    child.sendline ('%s' % secret_key)
    child.expect ('Default region name')
    child.sendline ('%s' % region_name)
    child.expect ('Default output format')
    child.sendline ('json')
    child.expect (pexpect.EOF)
    #print child.before, child.after

    print '3) Create a trusted policy to be able to perform certain AWS operation'
    file_trust_policy = open('trust-policy.json', 'w')
    s='''{
       "Version":"2012-10-17",
       "Statement":[
          {
             "Sid":"",
             "Effect":"Allow",
             "Principal":{
                "Service":"vmie.amazonaws.com"
             },
             "Action":"sts:AssumeRole",
             "Condition":{
                "StringEquals":{
                   "sts:ExternalId":"vmimport"
                }
             }
          }
       ]
    }'''
    file_trust_policy.write(s)
    file_trust_policy.close()
    
    print '4) Create a role named vmimport and give VM Import/Export access to it '
    pexpect.run('aws iam create-role --role-name vmimport --assume-role-policy-document file://trust-policy.json')

    print '5) Create a role policy to be able to perform certain AWS operation'
    file_role_policy = open('role-policy.json', 'w')
    s='''{
       "Version":"2012-10-17",
       "Statement":[
          {
             "Effect":"Allow",
             "Action":[
                "s3:ListBucket",
                "s3:GetBucketLocation"
             ],
             "Resource":[
                "arn:aws:s3:::'''+bucket_name+'''"
             ]
          },
          {
             "Effect":"Allow",
             "Action":[
                "s3:GetObject"
             ],
             "Resource":[
                "arn:aws:s3:::'''+bucket_name+'''/*"
             ]
          },
          {
             "Effect":"Allow",
             "Action":[
                "ec2:ModifySnapshotAttribute",
                "ec2:CopySnapshot",
                "ec2:RegisterImage",
                "ec2:Describe*"
             ],
             "Resource":"*"
          }
       ]
    }'''
    file_role_policy.write(s)
    file_role_policy.close()

    print '6) Attach the policy to the role '
    pexpect.run('aws iam put-role-policy --role-name vmimport --policy-name vmimport --policy-document file://role-policy.json')

    print '7) Create containers file, which contains information about the image'
    file_containers = open('containers.json', 'w')
    s='''[{
        "Description": "NSG-Build",
        "Format": "raw",
        "UserBucket": {
            "S3Bucket": "'''+bucket_name+'''",
            "S3Key": "'''+nsg_filename+'''"
        }
    }]'''
    file_containers.write(s)
    file_containers.close()

    print '8) Execute the role policy'
    output = pexpect.run('aws ec2 import-image --description "NSG-Build" --disk-containers file://containers.json')
    start='ImportTaskId": "'
    ami_id = (output.split(start))[1].split('"')[0]

    print '9) Remove the temp files (trust-policy.json, role-policy.json, containers.json)'
    pexpect.run('rm trust-policy.json') 
    pexpect.run('rm role-policy.json') 
    pexpect.run('rm containers.json') 

    print '10) Check the status of loading the AMI image to your EC2. This usually takes 20-30 minutes'
    while not "success" in output:
        progress_output = pexpect.run('aws ec2 describe-import-image-tasks --import-task-ids %s' % ami_id)
        time.sleep(120) # delays for 120 seconds
        progress_start='Progress": "'
        if progress_start in progress_output:
            progress = (progress_output.split(progress_start))[1].split('"')[0]
            print '    The progress on importing the image to EC2 is: "'+progress+'%"'
    
        if "completed" in progress_output:
            output = "success"   
    
    print '***********************************************************'
    print '***     Image has been successfully imported to EC2     ***'
    print '***********************************************************'


if __name__ == "__main__":
   main()
