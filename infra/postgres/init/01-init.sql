-- Create databases for different services
CREATE DATABASE user_service;
CREATE DATABASE product_catalog;
CREATE DATABASE order_management;

-- Create application user
CREATE USER app_user WITH PASSWORD 'app_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE user_service TO app_user;
GRANT ALL PRIVILEGES ON DATABASE product_catalog TO app_user;
GRANT ALL PRIVILEGES ON DATABASE order_management TO app_user;
