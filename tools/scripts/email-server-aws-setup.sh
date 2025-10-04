#!/bin/bash

# AWS Email Server Setup Script
# This script sets up the AWS infrastructure for a self-hosted email server

set -e

echo "=== AWS Email Server Infrastructure Setup ==="

# Variables - Update these with your values
DOMAIN_NAME="example.com"
MAIL_SUBDOMAIN="mail.${DOMAIN_NAME}"
REGION="us-east-1"
INSTANCE_TYPE="t3.medium"  # 2 vCPUs, 4GB RAM
KEY_PAIR_NAME="email-server-key"
VPC_CIDR="10.0.0.0/16"
SUBNET_CIDR="10.0.1.0/24"

echo "Setting up infrastructure for domain: $DOMAIN_NAME"
echo "Region: $REGION"

# 1. Create VPC and networking
echo "Creating VPC and networking..."
VPC_ID=$(aws ec2 create-vpc \
    --cidr-block $VPC_CIDR \
    --region $REGION \
    --query 'Vpc.VpcId' \
    --output text)

aws ec2 create-tags \
    --resources $VPC_ID \
    --tags Key=Name,Value=email-server-vpc \
    --region $REGION

# Enable DNS hostnames
aws ec2 modify-vpc-attribute \
    --vpc-id $VPC_ID \
    --enable-dns-hostnames \
    --region $REGION

# Create Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway \
    --region $REGION \
    --query 'InternetGateway.InternetGatewayId' \
    --output text)

aws ec2 attach-internet-gateway \
    --internet-gateway-id $IGW_ID \
    --vpc-id $VPC_ID \
    --region $REGION

# Create subnet
SUBNET_ID=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block $SUBNET_CIDR \
    --region $REGION \
    --query 'Subnet.SubnetId' \
    --output text)

aws ec2 create-tags \
    --resources $SUBNET_ID \
    --tags Key=Name,Value=email-server-subnet \
    --region $REGION

# Create route table
ROUTE_TABLE_ID=$(aws ec2 create-route-table \
    --vpc-id $VPC_ID \
    --region $REGION \
    --query 'RouteTable.RouteTableId' \
    --output text)

aws ec2 create-route \
    --route-table-id $ROUTE_TABLE_ID \
    --destination-cidr-block 0.0.0.0/0 \
    --gateway-id $IGW_ID \
    --region $REGION

aws ec2 associate-route-table \
    --subnet-id $SUBNET_ID \
    --route-table-id $ROUTE_TABLE_ID \
    --region $REGION

# 2. Create Security Group
echo "Creating security group..."
SG_ID=$(aws ec2 create-security-group \
    --group-name email-server-sg \
    --description "Security group for email server" \
    --vpc-id $VPC_ID \
    --region $REGION \
    --query 'GroupId' \
    --output text)

# Email server ports
PORTS=(22 25 80 110 143 443 465 587 993 995)
for port in "${PORTS[@]}"; do
    aws ec2 authorize-security-group-ingress \
        --group-id $SG_ID \
        --protocol tcp \
        --port $port \
        --cidr 0.0.0.0/0 \
        --region $REGION
done

# 3. Create RDS Subnet Group
echo "Creating RDS subnet group..."
# Create second subnet for RDS (different AZ)
SUBNET_ID_2=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block "10.0.2.0/24" \
    --availability-zone "${REGION}b" \
    --region $REGION \
    --query 'Subnet.SubnetId' \
    --output text)

aws ec2 create-tags \
    --resources $SUBNET_ID_2 \
    --tags Key=Name,Value=email-server-subnet-2 \
    --region $REGION

aws rds create-db-subnet-group \
    --db-subnet-group-name email-server-subnet-group \
    --db-subnet-group-description "Subnet group for email server database" \
    --subnet-ids $SUBNET_ID $SUBNET_ID_2 \
    --region $REGION

# 4. Create RDS Security Group
RDS_SG_ID=$(aws ec2 create-security-group \
    --group-name email-server-rds-sg \
    --description "Security group for email server RDS" \
    --vpc-id $VPC_ID \
    --region $REGION \
    --query 'GroupId' \
    --output text)

aws ec2 authorize-security-group-ingress \
    --group-id $RDS_SG_ID \
    --protocol tcp \
    --port 3306 \
    --source-group $SG_ID \
    --region $REGION

# 5. Launch RDS Instance
echo "Creating RDS instance..."
aws rds create-db-instance \
    --db-instance-identifier email-server-db \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --master-username mailuser \
    --master-user-password "$(openssl rand -base64 32)" \
    --allocated-storage 20 \
    --vpc-security-group-ids $RDS_SG_ID \
    --db-subnet-group-name email-server-subnet-group \
    --region $REGION

# 6. Allocate Elastic IP
echo "Allocating Elastic IP..."
EIP_ALLOC=$(aws ec2 allocate-address \
    --domain vpc \
    --region $REGION \
    --query 'AllocationId' \
    --output text)

EIP_ADDRESS=$(aws ec2 describe-addresses \
    --allocation-ids $EIP_ALLOC \
    --region $REGION \
    --query 'Addresses[0].PublicIp' \
    --output text)

# 7. Launch EC2 Instance
echo "Launching EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id ami-0c02fb55956c7d316 \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_PAIR_NAME \
    --security-group-ids $SG_ID \
    --subnet-id $SUBNET_ID \
    --associate-public-ip-address \
    --region $REGION \
    --query 'Instances[0].InstanceId' \
    --output text)

aws ec2 create-tags \
    --resources $INSTANCE_ID \
    --tags Key=Name,Value=email-server \
    --region $REGION

# Wait for instance to be running
echo "Waiting for instance to be running..."
aws ec2 wait instance-running \
    --instance-ids $INSTANCE_ID \
    --region $REGION

# Associate Elastic IP
aws ec2 associate-address \
    --instance-id $INSTANCE_ID \
    --allocation-id $EIP_ALLOC \
    --region $REGION

echo "=== Infrastructure Setup Complete ==="
echo "Instance ID: $INSTANCE_ID"
echo "Elastic IP: $EIP_ADDRESS"
echo "RDS Endpoint: (check AWS console after RDS is ready)"
echo ""
echo "Next steps:"
echo "1. Update your domain's DNS records:"
echo "   - A record: $MAIL_SUBDOMAIN -> $EIP_ADDRESS"
echo "   - MX record: $DOMAIN_NAME -> $MAIL_SUBDOMAIN"
echo "2. Set up reverse DNS (PTR record) with AWS support"
echo "3. Run the email server installation script on the EC2 instance"
