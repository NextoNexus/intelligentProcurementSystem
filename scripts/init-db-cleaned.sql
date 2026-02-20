-- 
-- PostgreSQL

-- UTF8
SET client_encoding = 'UTF8';

-- 
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 
SET search_path TO public;

-- Alembic
-- 

-- 
DO $$
BEGIN
    -- 
    INSERT INTO role (id, name, description, is_system, created_at, updated_at, is_deleted)
    VALUES
        (uuid_generate_v4(), 'admin', '系统管理员', true, NOW(), NOW(), false),
        (uuid_generate_v4(), 'department_head', '部门领导', true, NOW(), NOW(), false),
        (uuid_generate_v4(), 'management', '管理层', true, NOW(), NOW(), false),
        (uuid_generate_v4(), 'employee', '普通员工', true, NOW(), NOW(), false)
    ON CONFLICT (name) DO NOTHING;

    -- 
    INSERT INTO permission (id, code, name, description, module, created_at, updated_at, is_deleted)
    VALUES
        (uuid_generate_v4(), 'user:create', '创建用户', '可以创建新用户', 'user', NOW(), NOW(), false),
        (uuid_generate_v4(), 'user:read', '查看用户', '可以查看用户信息', 'user', NOW(), NOW(), false),
        (uuid_generate_v4(), 'user:update', '更新用户', '可以更新用户信息', 'user', NOW(), NOW(), false),
        (uuid_generate_v4(), 'user:delete', '删除用户', '可以删除用户', 'user', NOW(), NOW(), false),
        (uuid_generate_v4(), 'procurement:create', '创建采购需求', '可以创建采购需求', 'procurement', NOW(), NOW(), false),
        (uuid_generate_v4(), 'procurement:approve', '审批采购需求', '可以审批采购需求', 'procurement', NOW(), NOW(), false),
        (uuid_generate_v4(), 'supplier:create', '创建供应商', '可以创建供应商', 'supplier', NOW(), NOW(), false),
        (uuid_generate_v4(), 'supplier:read', '查看供应商', '可以查看供应商信息', 'supplier', NOW(), NOW(), false),
        (uuid_generate_v4(), 'inventory:read', '查看库存', '可以查看库存信息', 'inventory', NOW(), NOW(), false),
        (uuid_generate_v4(), 'inventory:update', '更新库存', '可以更新库存信息', 'inventory', NOW(), NOW(), false)
    ON CONFLICT (code) DO NOTHING;

    -- admin
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

    -- department_head
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

    -- management
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

    -- employee
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

    RAISE NOTICE '数据库初始化完成。已为系统角色分配默认权限。';
END
$$;