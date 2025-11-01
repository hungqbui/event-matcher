-- Setup script for creating test database and user
-- Run this as MySQL root user:
-- mysql -u root -p < db/setup_test_db.sql

-- Create the dev_user if it doesn't exist
CREATE USER IF NOT EXISTS 'dev_user'@'localhost' IDENTIFIED BY 'Team15';

-- Grant privileges on both production and test databases
GRANT ALL PRIVILEGES ON eventmatchers.* TO 'dev_user'@'localhost';
GRANT ALL PRIVILEGES ON eventmatcher_test.* TO 'dev_user'@'localhost';

-- Create test database if it doesn't exist
CREATE DATABASE IF NOT EXISTS eventmatcher_test;

-- Apply privileges
FLUSH PRIVILEGES;

-- Show the result
SELECT user, host FROM mysql.user WHERE user = 'dev_user';
SHOW DATABASES LIKE 'eventmatcher%';
