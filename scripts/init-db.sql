-- Database initialization script
-- This script should be executed automatically when PostgreSQL container starts

-- Set client encoding to UTF8
SET client_encoding = 'UTF8';

-- Create extension if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set search path
SET search_path TO public;

-- Note: Actual table structure will be created by Alembic migrations
-- Here we only create some initial data

-- Create system roles (if tables exist)
DO $$
BEGIN
    -- Insert system roles
    INSERT INTO role (id, name, description, is_system, created_at, updated_at, is_deleted)
    VALUES
        (uuid_generate_v4(), 'admin', 'System Administrator', true, NOW(), NOW(), false),
        (uuid_generate_v4(), 'department_head', 'Department Head', true, NOW(), NOW(), false),
        (uuid_generate_v4(), 'management', 'Management Level', true, NOW(), NOW(), false),
        (uuid_generate_v4(), 'employee', 'Regular Employee', true, NOW(), NOW(), false)
    ON CONFLICT (name) DO NOTHING;

    -- Insert system permissions (examples)
    INSERT INTO permission (id, code, name, description, module, created_at, updated_at, is_deleted)
    VALUES
        (uuid_generate_v4(), 'user:create', 'Create User', 'Can create new users', 'user', NOW(), NOW(), false),
        (uuid_generate_v4(), 'user:read', 'View User', 'Can view user information', 'user', NOW(), NOW(), false),
        (uuid_generate_v4(), 'user:update', 'Update User', 'Can update user information', 'user', NOW(), NOW(), false),
        (uuid_generate_v4(), 'user:delete', 'Delete User', 'Can delete users', 'user', NOW(), NOW(), false),
        (uuid_generate_v4(), 'procurement:create', 'Create Procurement Request', 'Can create procurement requests', 'procurement', NOW(), NOW(), false),
        (uuid_generate_v4(), 'procurement:approve', 'Approve Procurement Request', 'Can approve procurement requests', 'procurement', NOW(), NOW(), false),
        (uuid_generate_v4(), 'supplier:create', 'Create Supplier', 'Can create suppliers', 'supplier', NOW(), NOW(), false),
        (uuid_generate_v4(), 'supplier:read', 'View Supplier', 'Can view supplier information', 'supplier', NOW(), NOW(), false),
        (uuid_generate_v4(), 'inventory:read', 'View Inventory', 'Can view inventory information', 'inventory', NOW(), NOW(), false),
        (uuid_generate_v4(), 'inventory:update', 'Update Inventory', 'Can update inventory information', 'inventory', NOW(), NOW(), false)
    ON CONFLICT (code) DO NOTHING;

    -- Assign all permissions to admin role
    WITH admin_role AS (
        SELECT id FROM role WHERE name = 'admin' LIMIT 1
    ),
    all_permissions AS (
        SELECT id FROM permission
    )
    INSERT INTO role_permission (role_id, permission_id, created_at)
    SELECT admin_role.id, all_permissions.id, NOW()
    FROM admin_role, all_permissions
    ON CONFLICT (role_id, permission_id) DO NOTHING;

    -- Assign permissions to department_head role
    WITH department_head_role AS (
        SELECT id FROM role WHERE name = 'department_head' LIMIT 1
    ),
    department_head_permissions AS (
        SELECT id FROM permission
        WHERE code IN ('user:read', 'user:create', 'procurement:create', 'procurement:approve', 'supplier:read', 'inventory:read')
    )
    INSERT INTO role_permission (role_id, permission_id, created_at)
    SELECT department_head_role.id, department_head_permissions.id, NOW()
    FROM department_head_role, department_head_permissions
    ON CONFLICT (role_id, permission_id) DO NOTHING;

    -- Assign permissions to management role
    WITH management_role AS (
        SELECT id FROM role WHERE name = 'management' LIMIT 1
    ),
    management_permissions AS (
        SELECT id FROM permission
        WHERE code IN ('user:read', 'procurement:approve', 'supplier:read', 'inventory:read')
    )
    INSERT INTO role_permission (role_id, permission_id, created_at)
    SELECT management_role.id, management_permissions.id, NOW()
    FROM management_role, management_permissions
    ON CONFLICT (role_id, permission_id) DO NOTHING;

    -- Assign permissions to employee role
    WITH employee_role AS (
        SELECT id FROM role WHERE name = 'employee' LIMIT 1
    ),
    employee_permissions AS (
        SELECT id FROM permission
        WHERE code IN ('user:read', 'procurement:create', 'supplier:read', 'inventory:read')
    )
    INSERT INTO role_permission (role_id, permission_id, created_at)
    SELECT employee_role.id, employee_permissions.id, NOW()
    FROM employee_role, employee_permissions
    ON CONFLICT (role_id, permission_id) DO NOTHING;

    RAISE NOTICE 'Database initialization completed. Default permissions assigned to system roles.';
END
$$;