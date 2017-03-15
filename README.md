# import-image-to-ec2-aws
##Caution! Use it under your own risk. Intended for PoCs and Labs

#Createyour SD-WAN in a box (Nuage VNS)

Hello there. Bored to create and recreate many times my lab for SD-WAN using Nuage VNS. I've created this playbook Installing igateways, dns and ntp services, management and control planes in just one server with Centos7 KVM:

Create a dns/ntp/dhcp instance.
Nuage VSD ( management ) and a couple of VCSs (control).
Util server to bootstrap your NSGs
Stat to collect stats and apply Intelligence
Two NSG-vs as head ends at the Datacenter
Two independent NSG-vs as remote sites and a couple of clients behind
##Prepare your enviroment

Install docker and create an image as I show in the "Other otpion" at https://pinrojas.com/2017/02/07/ansible-docker-image-to-safely-run-my-playbooks-in-few-steps/

Quick Start

Step 1: Create Dummies/Bridges interfaces

Create your bridges and dummies interfaces if you plan to install this in one box. If you don't plan to use just one Box. Skip this step. Check _bridges.yml for settings details. _bridges.yml playbook will set your KVM server with the following:

Disable selinux
Enable forwarding
Disable NetworkManager and Firewall
Flush iptables and create NAT rules
Creat dummies and Bridges
Reboot KVM host
We'll create 5 bridges: core (as the datacenter), inet (internet), wan (as a WAN like a MPLS), branch1 and branch2.
