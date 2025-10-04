# AWS Email Server Deployment Guide

This guide walks you through deploying a complete, production-ready email server on AWS using the DIY Self-Hosted Email Server components.

## 🏗️ Architecture Overview

**AWS Services Used:**
- **EC2**: Email server instance (Postfix, Dovecot, etc.)
- **RDS MySQL**: User database and email storage metadata
- **Route 53**: DNS management
- **Certificate Manager**: SSL/TLS certificates (optional)
- **Elastic IP**: Static IP address
- **VPC**: Isolated network environment
- **Security Groups**: Firewall rules
- **CloudWatch**: Monitoring and logging

## 📋 Prerequisites

1. **AWS Account** with appropriate permissions
2. **Domain name** with ability to modify DNS records
3. **AWS CLI** configured with your credentials
4. **Clean IP reputation** (new AWS account recommended)

## 🚀 Deployment Options

### Option 1: CloudFormation (Recommended)

Deploy the complete infrastructure with one command:

```bash
# Deploy the CloudFormation stack
aws cloudformation create-stack \
  --stack-name email-server \
  --template-body file://email-server-cloudformation.yaml \
  --parameters ParameterKey=DomainName,ParameterValue=yourdomain.com \
               ParameterKey=KeyPairName,ParameterValue=your-key-pair \
               ParameterKey=DBPassword,ParameterValue=your-secure-password \
  --capabilities CAPABILITY_IAM
```

### Option 2: Manual Setup

Run the infrastructure setup script:

```bash
# Make the script executable
chmod +x email-server-aws-setup.sh

# Edit the variables in the script
nano email-server-aws-setup.sh

# Run the setup
./email-server-aws-setup.sh
```

## 📧 Post-Deployment Configuration

### 1. Configure Reverse DNS (PTR Record)

**Critical for deliverability!**

Contact AWS Support to set up reverse DNS:
1. Open AWS Support case
2. Request PTR record: `your-elastic-ip` → `mail.yourdomain.com`
3. Wait for confirmation (usually 24-48 hours)

### 2. SSH to Your Server

```bash
# Get your server's IP from CloudFormation outputs
aws cloudformation describe-stacks \
  --stack-name email-server \
  --query 'Stacks[0].Outputs'

# SSH to the server
ssh -i your-key.pem ubuntu@your-elastic-ip
```

### 3. Run Email Server Installation

```bash
# Download and run the installation script
wget https://raw.githubusercontent.com/your-repo/install-email-server.sh
chmod +x install-email-server.sh

# Edit configuration variables
sudo nano install-email-server.sh

# Run installation (takes 10-15 minutes)
sudo ./install-email-server.sh
```

### 4. Set Up Database

```bash
# Connect to RDS and run database setup
mysql -h your-rds-endpoint -u mailuser -p < setup-database.sql

# Generate password hash for your admin user
doveadm pw -s SHA512-CRYPT

# Update the database with your actual admin user
mysql -h your-rds-endpoint -u mailuser -p
```

### 5. Configure DNS Records

Add these DNS records to your domain:

```dns
# A Record
mail.yourdomain.com.    IN  A       your-elastic-ip

# MX Record  
yourdomain.com.         IN  MX  10  mail.yourdomain.com.

# SPF Record
yourdomain.com.         IN  TXT     "v=spf1 a mx ip4:your-elastic-ip ~all"

# DKIM Record (get from server)
mail._domainkey.yourdomain.com. IN TXT "v=DKIM1; k=rsa; p=YOUR_PUBLIC_KEY"

# DMARC Record
_dmarc.yourdomain.com.  IN  TXT     "v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@yourdomain.com"
```

### 6. Get DKIM Public Key

```bash
# On your server, get the DKIM public key
sudo cat /etc/opendkim/keys/yourdomain.com/mail.txt
```

## 🔧 AWS-Specific Optimizations

### 1. SES Integration (Optional)

For better deliverability, configure SES as a backup relay:

```bash
# Install SES SMTP credentials
sudo postconf -e 'relayhost = [email-smtp.us-east-1.amazonaws.com]:587'
sudo postconf -e 'smtp_sasl_auth_enable = yes'
sudo postconf -e 'smtp_sasl_security_options = noanonymous'
sudo postconf -e 'smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd'

# Create SASL password file
echo '[email-smtp.us-east-1.amazonaws.com]:587 YOUR_SES_USERNAME:YOUR_SES_PASSWORD' | sudo tee /etc/postfix/sasl_passwd
sudo postmap /etc/postfix/sasl_passwd
sudo chmod 600 /etc/postfix/sasl_passwd*
```

### 2. CloudWatch Monitoring

```bash
# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb

# Configure monitoring for email logs
sudo tee /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json > /dev/null <<EOF
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/mail.log",
            "log_group_name": "/aws/ec2/email-server/mail",
            "log_stream_name": "{instance_id}"
          },
          {
            "file_path": "/var/log/dovecot.log",
            "log_group_name": "/aws/ec2/email-server/dovecot",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  }
}
EOF

sudo systemctl enable amazon-cloudwatch-agent
sudo systemctl start amazon-cloudwatch-agent
```

### 3. Automated Backups

```bash
# Create backup script
sudo tee /usr/local/bin/email-backup.sh > /dev/null <<EOF
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/email"
S3_BUCKET="your-backup-bucket"

mkdir -p $BACKUP_DIR

# Backup mail data
tar -czf $BACKUP_DIR/mail_data_$DATE.tar.gz /var/mail/vhosts

# Backup configurations
tar -czf $BACKUP_DIR/mail_config_$DATE.tar.gz /etc/postfix /etc/dovecot /etc/opendkim

# Upload to S3
aws s3 cp $BACKUP_DIR/ s3://$S3_BUCKET/email-backups/ --recursive

# Clean old local backups (keep 7 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

chmod +x /usr/local/bin/email-backup.sh

# Add to crontab (daily at 2 AM)
echo "0 2 * * * /usr/local/bin/email-backup.sh" | sudo crontab -
```

## 🔍 Testing Your Setup

### 1. Test Email Sending

```bash
# Send test email
echo "Test email body" | mail -s "Test Subject" test@gmail.com
```

### 2. Test Email Receiving

```bash
# Check if email is received
sudo tail -f /var/log/mail.log
```

### 3. Test Webmail Access

Visit: `https://mail.yourdomain.com/roundcube`

### 4. Test Deliverability

Use these tools:
- [Mail Tester](https://www.mail-tester.com/)
- [MXToolbox](https://mxtoolbox.com/)
- [DMARC Analyzer](https://www.dmarcanalyzer.com/)

## 💰 Cost Estimation

**Monthly AWS costs (us-east-1):**
- EC2 t3.medium: ~$30
- RDS db.t3.micro: ~$15
- Elastic IP: ~$4
- Data transfer: ~$5-10
- **Total: ~$54-59/month**

## 🛡️ Security Best Practices

### 1. Regular Updates

```bash
# Set up automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 2. Firewall Configuration

```bash
# Configure UFW (additional to Security Groups)
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 25,80,110,143,443,465,587,993,995/tcp
```

### 3. Intrusion Detection

```bash
# Install and configure AIDE
sudo apt install aide
sudo aideinit
sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# Add to crontab for daily checks
echo "0 3 * * * /usr/bin/aide --check" | sudo crontab -
```

## 📊 Monitoring and Maintenance

### Key Metrics to Monitor

1. **Email Queue Size**: `mailq | wc -l`
2. **Disk Usage**: `df -h`
3. **Memory Usage**: `free -m`
4. **Failed Login Attempts**: `grep "authentication failed" /var/log/dovecot.log`
5. **Spam Detection Rate**: `grep "SPAM" /var/log/mail.log | wc -l`

### Regular Maintenance Tasks

1. **Weekly**: Review logs for errors
2. **Monthly**: Update spam filters and virus definitions
3. **Quarterly**: Review and update DNS records
4. **Annually**: Renew SSL certificates (if not using Let's Encrypt)

## 🆘 Troubleshooting

### Common Issues

1. **Emails going to spam**:
   - Check SPF, DKIM, DMARC records
   - Verify reverse DNS is set up
   - Check IP reputation

2. **Cannot receive emails**:
   - Verify MX record
   - Check firewall rules
   - Review mail.log for errors

3. **SSL certificate issues**:
   - Ensure domain points to server IP
   - Check Let's Encrypt rate limits
   - Verify DNS propagation

### Log Files to Check

```bash
# Main mail log
sudo tail -f /var/log/mail.log

# Dovecot log
sudo tail -f /var/log/dovecot.log

# Nginx log
sudo tail -f /var/log/nginx/error.log

# System log
sudo tail -f /var/log/syslog
```

## 🎯 Performance Tuning

### For Higher Volumes

1. **Upgrade instance type** to t3.large or c5.large
2. **Use RDS Multi-AZ** for high availability
3. **Implement Redis** for session caching
4. **Configure Postfix** for higher concurrency
5. **Use EFS** for shared mail storage across instances

This AWS deployment gives you a robust, scalable email server that matches commercial providers while maintaining full control over your data and configuration.
