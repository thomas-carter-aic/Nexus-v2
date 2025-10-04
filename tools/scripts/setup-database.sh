#!/bin/bash

# PostgreSQL Database Setup Script for Job Application System
# This script sets up the PostgreSQL database and user for the AIC careers system

set -e

echo "🚀 Setting up PostgreSQL database for AIC Job Application System..."

# Database configuration
DB_NAME="aic_careers"
DB_USER="aic_user"
DB_PASSWORD="aic_password"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed. Installing PostgreSQL..."
    
    # Detect OS and install PostgreSQL
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Ubuntu/Debian
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y postgresql postgresql-contrib
        # CentOS/RHEL/Fedora
        elif command -v yum &> /dev/null; then
            sudo yum install -y postgresql-server postgresql-contrib
            sudo postgresql-setup initdb
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y postgresql-server postgresql-contrib
            sudo postgresql-setup --initdb
        fi
        
        # Start PostgreSQL service
        sudo systemctl start postgresql
        sudo systemctl enable postgresql
        
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install postgresql
            brew services start postgresql
        else
            echo "❌ Homebrew not found. Please install PostgreSQL manually."
            exit 1
        fi
    else
        echo "❌ Unsupported operating system. Please install PostgreSQL manually."
        exit 1
    fi
fi

echo "✅ PostgreSQL is installed"

# Check if PostgreSQL service is running
if ! pgrep -x "postgres" > /dev/null; then
    echo "🔄 Starting PostgreSQL service..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo systemctl start postgresql
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew services start postgresql
    fi
fi

echo "✅ PostgreSQL service is running"

# Create database and user
echo "🔄 Creating database and user..."

# Function to run SQL commands
run_sql() {
    sudo -u postgres psql -c "$1"
}

# Create user if it doesn't exist
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
    echo "Creating user: $DB_USER"
    run_sql "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
else
    echo "User $DB_USER already exists"
fi

# Create database if it doesn't exist
if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "Creating database: $DB_NAME"
    run_sql "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
else
    echo "Database $DB_NAME already exists"
fi

# Grant privileges
echo "Granting privileges..."
run_sql "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
run_sql "ALTER USER $DB_USER CREATEDB;"

echo "✅ Database setup completed successfully!"

# Test connection
echo "🔄 Testing database connection..."
if PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $DB_NAME -c "SELECT version();" > /dev/null 2>&1; then
    echo "✅ Database connection test successful!"
else
    echo "❌ Database connection test failed!"
    exit 1
fi

echo ""
echo "📋 Database Configuration Summary:"
echo "  Database Name: $DB_NAME"
echo "  Username: $DB_USER"
echo "  Password: $DB_PASSWORD"
echo "  Host: localhost"
echo "  Port: 5432"
echo ""
echo "🔗 Connection String:"
echo "  DATABASE_URL=\"postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME?schema=public\""
echo ""
echo "🎉 PostgreSQL setup complete! You can now run 'npm run db:migrate' to set up the database schema."
