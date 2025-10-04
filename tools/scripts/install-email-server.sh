#!/bin/bash

# Email Server Installation Script for AWS
# Based on the DIY Self-Hosted Email Server Guide

set -e

# Configuration variables - UPDATE THESE
DOMAIN="example.com"
MAIL_HOSTNAME="mail.${DOMAIN}"
DB_HOST="your-rds-endpoint.region.rds.amazonaws.com"
DB_PASSWORD="your-rds-password"
ADMIN_EMAIL="admin@${DOMAIN}"

echo "=== Installing Email Server Components ==="
echo "Domain: $DOMAIN"
echo "Mail hostname: $MAIL_HOSTNAME"

# 1. System preparation
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

# Set hostname
sudo hostnamectl set-hostname $MAIL_HOSTNAME

# Update /etc/hosts
echo "127.0.0.1 localhost" | sudo tee /etc/hosts
echo "$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4) $MAIL_HOSTNAME mail" | sudo tee -a /etc/hosts

# 2. Install all required packages
echo "Installing packages..."
sudo DEBIAN_FRONTEND=noninteractive apt install -y \
    postfix postfix-mysql \
    dovecot-core dovecot-imapd dovecot-pop3d dovecot-lmtpd dovecot-mysql \
    spamassassin spamc \
    clamav clamav-daemon \
    amavisd-new \
    opendkim opendkim-tools \
    nginx \
    php-fpm php-mysql php-mbstring php-xml php-curl \
    mysql-client \
    certbot python3-certbot-nginx \
    fail2ban \
    roundcube roundcube-mysql \
    unzip wget curl

# 3. Configure Postfix
echo "Configuring Postfix..."
sudo tee /etc/postfix/main.cf > /dev/null <<EOF
# Basic configuration
myhostname = $MAIL_HOSTNAME
mydomain = $DOMAIN
myorigin = \$mydomain
mydestination = \$myhostname, localhost.\$mydomain, localhost
mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
mailbox_size_limit = 0
recipient_delimiter = +
inet_interfaces = all
inet_protocols = all

# TLS configuration
smtpd_tls_cert_file = /etc/letsencrypt/live/$MAIL_HOSTNAME/fullchain.pem
smtpd_tls_key_file = /etc/letsencrypt/live/$MAIL_HOSTNAME/privkey.pem
smtpd_use_tls = yes
smtpd_tls_auth_only = yes
smtp_tls_security_level = may
smtpd_tls_protocols = !SSLv2,!SSLv3,!TLSv1,!TLSv1.1
smtpd_tls_ciphers = medium
smtpd_tls_exclude_ciphers = MD5, SRP, PSK, aNull, aNULL, eNULL, EXPORT, DES, RC4, 3DES, ADH, LOW@STRENGTH

# SASL authentication
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous
smtpd_sasl_local_domain = \$myhostname

# Virtual mailbox configuration
virtual_mailbox_domains = mysql:/etc/postfix/mysql-virtual-mailbox-domains.cf
virtual_mailbox_maps = mysql:/etc/postfix/mysql-virtual-mailbox-maps.cf
virtual_alias_maps = mysql:/etc/postfix/mysql-virtual-alias-maps.cf
virtual_mailbox_base = /var/mail/vhosts
virtual_uid_maps = static:5000
virtual_gid_maps = static:5000

# Security restrictions
smtpd_recipient_restrictions =
    permit_sasl_authenticated,
    permit_mynetworks,
    reject_unauth_destination,
    reject_rbl_client zen.spamhaus.org,
    reject_rbl_client bl.spamcop.net,
    reject_rbl_client cbl.abuseat.org

# Content filtering
content_filter = amavis:[127.0.0.1]:10024
receive_override_options = no_address_mappings

# DKIM
smtpd_milters = inet:localhost:8891
non_smtpd_milters = \$smtpd_milters
milter_default_action = accept
EOF

# Create MySQL configuration files for Postfix
sudo tee /etc/postfix/mysql-virtual-mailbox-domains.cf > /dev/null <<EOF
user = mailuser
password = $DB_PASSWORD
hosts = $DB_HOST
dbname = mailserver
query = SELECT 1 FROM virtual_domains WHERE name='%s'
EOF

sudo tee /etc/postfix/mysql-virtual-mailbox-maps.cf > /dev/null <<EOF
user = mailuser
password = $DB_PASSWORD
hosts = $DB_HOST
dbname = mailserver
query = SELECT 1 FROM virtual_users WHERE email='%s'
EOF

sudo tee /etc/postfix/mysql-virtual-alias-maps.cf > /dev/null <<EOF
user = mailuser
password = $DB_PASSWORD
hosts = $DB_HOST
dbname = mailserver
query = SELECT destination FROM virtual_aliases WHERE source='%s'
EOF

# Set permissions
sudo chmod 640 /etc/postfix/mysql-*.cf
sudo chown root:postfix /etc/postfix/mysql-*.cf

# Configure master.cf for content filtering
sudo tee -a /etc/postfix/master.cf > /dev/null <<EOF

# Amavis content filter
amavis    unix  -       -       -       -       2       smtp
    -o smtp_data_done_timeout=1200
    -o smtp_send_xforward_command=yes
    -o disable_dns_lookups=yes

127.0.0.1:10025 inet  n  -       -       -       -       smtpd
    -o content_filter=
    -o local_recipient_maps=
    -o relay_recipient_maps=
    -o smtpd_restriction_classes=
    -o smtpd_client_restrictions=
    -o smtpd_helo_restrictions=
    -o smtpd_sender_restrictions=
    -o smtpd_recipient_restrictions=permit_mynetworks,reject
    -o mynetworks=127.0.0.0/8
    -o strict_rfc821_envelopes=yes
EOF

# 4. Configure Dovecot
echo "Configuring Dovecot..."
sudo tee /etc/dovecot/dovecot.conf > /dev/null <<EOF
protocols = imap pop3 lmtp
listen = *, ::
base_dir = /var/run/dovecot/
instance_name = dovecot
login_greeting = Dovecot ready.
EOF

sudo tee /etc/dovecot/conf.d/10-mail.conf > /dev/null <<EOF
mail_location = maildir:/var/mail/vhosts/%d/%n
mail_privileged_group = mail
mail_uid = 5000
mail_gid = 5000
first_valid_uid = 5000
last_valid_uid = 5000
first_valid_gid = 5000
last_valid_gid = 5000
EOF

sudo tee /etc/dovecot/conf.d/10-auth.conf > /dev/null <<EOF
disable_plaintext_auth = yes
auth_mechanisms = plain login
!include auth-sql.conf.ext
EOF

sudo tee /etc/dovecot/conf.d/auth-sql.conf.ext > /dev/null <<EOF
passdb {
  driver = sql
  args = /etc/dovecot/dovecot-sql.conf.ext
}
userdb {
  driver = static
  args = uid=5000 gid=5000 home=/var/mail/vhosts/%d/%n
}
EOF

sudo tee /etc/dovecot/dovecot-sql.conf.ext > /dev/null <<EOF
driver = mysql
connect = host=$DB_HOST dbname=mailserver user=mailuser password=$DB_PASSWORD
default_pass_scheme = SHA512-CRYPT
password_query = SELECT email as user, password FROM virtual_users WHERE email='%u';
EOF

sudo tee /etc/dovecot/conf.d/10-ssl.conf > /dev/null <<EOF
ssl = required
ssl_cert = </etc/letsencrypt/live/$MAIL_HOSTNAME/fullchain.pem
ssl_key = </etc/letsencrypt/live/$MAIL_HOSTNAME/privkey.pem
ssl_protocols = !SSLv3 !TLSv1 !TLSv1.1
ssl_cipher_list = ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256
ssl_prefer_server_ciphers = yes
ssl_dh = </etc/dovecot/dh.pem
EOF

sudo tee /etc/dovecot/conf.d/10-master.conf > /dev/null <<EOF
service imap-login {
  inet_listener imap {
    port = 143
  }
  inet_listener imaps {
    port = 993
    ssl = yes
  }
}

service pop3-login {
  inet_listener pop3 {
    port = 110
  }
  inet_listener pop3s {
    port = 995
    ssl = yes
  }
}

service lmtp {
  unix_listener /var/spool/postfix/private/dovecot-lmtp {
    mode = 0600
    user = postfix
    group = postfix
  }
}

service auth {
  unix_listener /var/spool/postfix/private/auth {
    mode = 0666
    user = postfix
    group = postfix
  }
  unix_listener auth-userdb {
    mode = 0600
    user = 5000
    group = 5000
  }
}

service auth-worker {
  user = 5000
}
EOF

# Generate DH parameters
sudo openssl dhparam -out /etc/dovecot/dh.pem 2048

# Set permissions
sudo chmod 600 /etc/dovecot/dovecot-sql.conf.ext
sudo chown dovecot:dovecot /etc/dovecot/dovecot-sql.conf.ext

# 5. Create mail directories
echo "Creating mail directories..."
sudo mkdir -p /var/mail/vhosts
sudo groupadd -g 5000 vmail
sudo useradd -g vmail -u 5000 vmail -d /var/mail/vhosts -s /sbin/nologin
sudo chown -R vmail:vmail /var/mail/vhosts

# 6. Configure SpamAssassin
echo "Configuring SpamAssassin..."
sudo tee /etc/spamassassin/local.cf > /dev/null <<EOF
report_safe 0
required_score 5.0
rewrite_header Subject *****SPAM*****
use_bayes 1
bayes_auto_learn 1
skip_rbl_checks 0
use_razor2 1
use_pyzor 1
use_dcc 1
EOF

sudo systemctl enable spamassassin
sudo systemctl start spamassassin

# 7. Configure ClamAV
echo "Configuring ClamAV..."
sudo freshclam
sudo systemctl enable clamav-daemon
sudo systemctl start clamav-daemon

# 8. Configure Amavis
echo "Configuring Amavis..."
sudo tee /etc/amavis/conf.d/15-content_filter_mode > /dev/null <<EOF
use strict;

@bypass_virus_checks_maps = (
   \%bypass_virus_checks, \@bypass_virus_checks_acl, \$bypass_virus_checks_re);

@bypass_spam_checks_maps = (
   \%bypass_spam_checks, \@bypass_spam_checks_acl, \$bypass_spam_checks_re);

1;
EOF

sudo tee /etc/amavis/conf.d/50-user > /dev/null <<EOF
use strict;

\$max_servers = 2;
\$daemon_user  = "amavis";
\$daemon_group = "amavis";
\$mydomain = "$DOMAIN";
\$myhostname = "$MAIL_HOSTNAME";

@local_domains_maps = ( [".$DOMAIN"] );

\$sa_tag_level_deflt  = 2.0;
\$sa_tag2_level_deflt = 6.2;
\$sa_kill_level_deflt = 6.9;
\$sa_dsn_cutoff_level = 10;

1;
EOF

sudo systemctl enable amavis
sudo systemctl start amavis

# 9. Configure OpenDKIM
echo "Configuring OpenDKIM..."
sudo mkdir -p /etc/opendkim/keys/$DOMAIN
sudo opendkim-genkey -s mail -d $DOMAIN -D /etc/opendkim/keys/$DOMAIN
sudo chown -R opendkim:opendkim /etc/opendkim/keys

sudo tee /etc/opendkim.conf > /dev/null <<EOF
Syslog yes
UMask 002
Domain $DOMAIN
KeyFile /etc/opendkim/keys/$DOMAIN/mail.private
Selector mail
Socket inet:8891@localhost
PidFile /var/run/opendkim/opendkim.pid
TrustAnchorFile /usr/share/dns/root.key
UserID opendkim
EOF

sudo systemctl enable opendkim
sudo systemctl start opendkim

# 10. Get SSL certificates
echo "Getting SSL certificates..."
sudo certbot certonly --standalone -d $MAIL_HOSTNAME --agree-tos --email $ADMIN_EMAIL --non-interactive

# 11. Configure Nginx
echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/$MAIL_HOSTNAME > /dev/null <<EOF
server {
    listen 80;
    server_name $MAIL_HOSTNAME;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $MAIL_HOSTNAME;
    
    ssl_certificate /etc/letsencrypt/live/$MAIL_HOSTNAME/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$MAIL_HOSTNAME/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    root /var/www/html;
    index index.php index.html index.htm;
    
    location / {
        try_files \$uri \$uri/ /index.php?\$args;
    }
    
    location ~ \.php\$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name;
        include fastcgi_params;
    }
    
    location /roundcube {
        alias /var/lib/roundcube/public_html;
        index index.php;
        
        location ~ \.php\$ {
            include snippets/fastcgi-php.conf;
            fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
            fastcgi_param SCRIPT_FILENAME \$request_filename;
            include fastcgi_params;
        }
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/$MAIL_HOSTNAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx

# 12. Configure Roundcube
echo "Configuring Roundcube..."
sudo tee /etc/roundcube/config.inc.php > /dev/null <<EOF
<?php
\$config = array();
\$config['db_dsnw'] = 'mysql://roundcube:roundcube@$DB_HOST/roundcube';
\$config['default_host'] = 'ssl://$MAIL_HOSTNAME';
\$config['default_port'] = 993;
\$config['smtp_server'] = 'ssl://$MAIL_HOSTNAME';
\$config['smtp_port'] = 465;
\$config['smtp_user'] = '%u';
\$config['smtp_pass'] = '%p';
\$config['support_url'] = '';
\$config['product_name'] = 'Webmail';
\$config['des_key'] = '$(openssl rand -hex 24)';
\$config['plugins'] = array('archive', 'zipdownload');
\$config['skin'] = 'elastic';
\$config['language'] = 'en_US';
\$config['session_lifetime'] = 10;
\$config['ip_check'] = true;
\$config['referer_check'] = true;
EOF

# 13. Configure Fail2Ban
echo "Configuring Fail2Ban..."
sudo tee /etc/fail2ban/jail.local > /dev/null <<EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[dovecot]
enabled = true
port = pop3,pop3s,imap,imaps
filter = dovecot
logpath = /var/log/dovecot.log

[postfix]
enabled = true
port = smtp,ssmtp,submission
filter = postfix
logpath = /var/log/mail.log

[postfix-sasl]
enabled = true
port = smtp,ssmtp,submission,imap2,imap3,imaps,pop3,pop3s
filter = postfix-sasl
logpath = /var/log/mail.log
EOF

sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# 14. Start and enable services
echo "Starting services..."
sudo systemctl enable postfix dovecot
sudo systemctl restart postfix dovecot

echo "=== Installation Complete ==="
echo ""
echo "Next steps:"
echo "1. Set up the database tables (run setup-database.sql)"
echo "2. Configure DNS records:"
echo "   - DKIM record: $(sudo cat /etc/opendkim/keys/$DOMAIN/mail.txt)"
echo "   - SPF record: v=spf1 a mx ip4:$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4) ~all"
echo "   - DMARC record: v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@$DOMAIN"
echo "3. Test email functionality"
echo "4. Access webmail at https://$MAIL_HOSTNAME/roundcube"
echo ""
echo "Log files to monitor:"
echo "- /var/log/mail.log"
echo "- /var/log/dovecot.log"
echo "- /var/log/nginx/error.log"
