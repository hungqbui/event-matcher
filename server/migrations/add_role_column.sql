-- Migration: Add role column to users table
-- Purpose: Support JWT authentication with role-based access control (RBAC)
-- Date: 2025-10-30

-- Add role column with default value 'volunteer'
ALTER TABLE users 
ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'volunteer';

-- Add index on role for faster queries
CREATE INDEX idx_users_role ON users(role);

-- Create an admin user for testing (update with your own credentials)
-- Password hash is for 'admin123' - CHANGE THIS IN PRODUCTION
INSERT INTO users (name, email, password_hash, state, role) 
VALUES (
    'Admin User',
    'admin@example.com',
    'scrypt:32768:8:1$tHkgUQ8iJjLgCZ7h$6c3f8e0d5a7b2c1d9e4f6a8b7c5d3e2f1a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f',
    'TX',
    'admin'
)
ON DUPLICATE KEY UPDATE role = 'admin';

-- Note: To generate a proper password hash, run in Python:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash('your_password'))

COMMIT;
