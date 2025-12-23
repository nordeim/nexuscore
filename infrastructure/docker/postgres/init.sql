-- NexusCore PostgreSQL Initialization
-- This script runs when the postgres container is first created

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set timezone to Singapore
SET timezone = 'Asia/Singapore';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE nexuscore TO nexuscore_user;
