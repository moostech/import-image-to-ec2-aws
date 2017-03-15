##Caution! Use it under your own risk. Intended for Nuage VNS PoCs and Labs

#Import NSG RAW Image from S3 to your Amazon EC2 account

Hello there. Bored from manually importing the RAW VM image from your S3 to your Amazon EC2. Don't worry, I've created a python script that will convert your image in few seconds. The script will do the following:

1. Install AWS CLI (if it is not installed already)
2. Create a role policy and a trusted entitiy to be able to perform certain AWS operation (i.e., downloading RAW images from Amazon S3 bucket)
3. Import the RAW Image
4. Check the status of the import-task

##Prepare your enviroment
Collect the following information to be used by the script
* Access Key ID
* Secret Access Key
* NSG AMI file name
* NSG AMI region (i.e., us-west-1)

# Quick Start

## Step 1: Create Dummies/Bridges interfaces

Create your bridges and dummies interfaces if you plan to install this in one box. If you don't plan to use just one Box. Skip this step. Check _bridges.yml for settings details. _bridges.yml playbook will set your KVM server with the following:

Disable selinux
Enable forwarding
