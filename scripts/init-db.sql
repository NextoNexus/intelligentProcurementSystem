-- 初始化数据库脚本
-- 在PostgreSQL容器启动时自动执行

-- 创建扩展（如果需要）
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 设置搜索路径
SET search_path TO public;

-- 注释：实际表结构将由Alembic迁移创建
-- 这里只创建一些初始数据

-- 创建系统角色（如果表已存在）
DO $$
BEGIN
    -- 插入系统角色
    INSERT INTO role (id, name, description, is_system, created_at, updated_at, is_deleted)
    VALUES
        (uuid_generate_v4(), 'admin', '系统管理员', true, NOW(), NOW(), false),
        (uuid_generate_v4(), 'manager', '部门经理', true, NOW(), NOW(), false),
        (uuid_generate_v4(), 'employee', '普通员工', true, NOW(), NOW(), false)
    ON CONFLICT (name) DO NOTHING;

    -- 插入系统权限（示例）
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

    -- 为角色分配权限（示例）
    -- 注意：这里需要先查询角色的ID，但在SQL中简化处理
    -- 实际应用中应该在应用层处理
    RAISE NOTICE '数据库初始化完成。请在应用启动后通过管理界面配置角色权限。';
END
$$;