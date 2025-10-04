-- Email Server Database Setup
-- Run this on your RDS MySQL instance

-- Create the main mailserver database
CREATE DATABASE IF NOT EXISTS mailserver;
USE mailserver;

-- Create tables for virtual domains, users, and aliases
CREATE TABLE IF NOT EXISTS virtual_domains (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY name (name)
);

CREATE TABLE IF NOT EXISTS virtual_users (
    id INT NOT NULL AUTO_INCREMENT,
    domain_id INT NOT NULL,
    password VARCHAR(106) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY email (email),
    FOREIGN KEY (domain_id) REFERENCES virtual_domains(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS virtual_aliases (
    id INT NOT NULL AUTO_INCREMENT,
    domain_id INT NOT NULL,
    source VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (domain_id) REFERENCES virtual_domains(id) ON DELETE CASCADE
);

-- Create Roundcube database
CREATE DATABASE IF NOT EXISTS roundcube;

-- Create user for mail services
CREATE USER IF NOT EXISTS 'mailuser'@'%' IDENTIFIED BY 'your-secure-password-here';
GRANT ALL PRIVILEGES ON mailserver.* TO 'mailuser'@'%';

-- Create user for Roundcube
CREATE USER IF NOT EXISTS 'roundcube'@'%' IDENTIFIED BY 'roundcube-password-here';
GRANT ALL PRIVILEGES ON roundcube.* TO 'roundcube'@'%';

FLUSH PRIVILEGES;

-- Insert sample domain (replace with your actual domain)
INSERT INTO virtual_domains (name) VALUES ('example.com');

-- Insert sample user (replace with actual email and generate proper password hash)
-- Password hash can be generated with: doveadm pw -s SHA512-CRYPT
INSERT INTO virtual_users (domain_id, password, email) VALUES 
(1, '{SHA512-CRYPT}$6$rounds=5000$your-salt-here$your-hash-here', 'admin@example.com');

-- Insert sample alias
INSERT INTO virtual_aliases (domain_id, source, destination) VALUES 
(1, 'postmaster@example.com', 'admin@example.com'),
(1, 'abuse@example.com', 'admin@example.com'),
(1, 'hostmaster@example.com', 'admin@example.com');

-- Show created structure
SHOW TABLES;
SELECT * FROM virtual_domains;
SELECT * FROM virtual_users;
SELECT * FROM virtual_aliases;
