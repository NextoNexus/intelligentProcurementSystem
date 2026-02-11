# 企业智能物资采购管理系统

## 项目简介

智能物资采购管理系统是一个基于Python FastAPI和Vue 3的现代化企业采购管理平台。系统集成了供应商管理、采购流程管理、库存控制、财务核算和AI智能聊天助手等功能。

## 技术栈

### 后端
- **框架**: FastAPI (Python 3.11+)
- **数据库**: PostgreSQL 18 + SQLAlchemy 2.0 + Alembic
- **认证**: JWT + OAuth2
- **AI集成**: pydantic_ai + OpenAI/Anthropic API
- **包管理**: uv

### 前端
- **框架**: Vue 3 + Composition API
- **样式**: Tailwind CSS 4
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **构建工具**: Vite

### 部署
- **容器化**: Docker + docker-compose
- **环境**: Windows 10+/Ubuntu 22.04+
- **数据库**: PostgreSQL 18

## 功能模块

### 核心功能（MVP）
1. **用户管理与权限控制**
   - 基于角色的访问控制（RBAC）
   - 4种用户角色：管理员、部门领导、管理层、员工
   - JWT认证与授权

2. **供应商管理**
   - 供应商注册与信息管理
   - 供应商评估与评级
   - 产品目录管理

3. **采购管理**
   - 采购需求提交与审批流程
   - 采购订单创建与管理
   - 订单状态跟踪

4. **库存管理**
   - 库存分类与查询
   - 入库出库管理
   - 库存预警

5. **AI智能聊天**
   - 文本聊天功能
   - 只读数据库查询
   - 可扩展MCP服务器支持

### 高级功能（后续迭代）
1. 财务管理与成本核算
2. 业务分析与报表系统
3. 供应商协同平台
4. 移动端适配

## 项目结构

```
intelligentProcurementSystem/
├── app/                    # 后端应用代码
│   ├── api/               # API路由模块
│   ├── core/              # 核心配置
│   ├── models/            # 数据库模型
│   ├── schemas/           # Pydantic验证模型
│   ├── services/          # 业务逻辑层
│   ├── ai/                # AI集成模块
│   └── migrations/        # 数据库迁移
├── frontend/              # 前端应用代码
├── tests/                 # 测试代码
├── docs/                  # 项目文档
└── scripts/               # 部署脚本
```

## 快速开始

### 环境要求
- Python 3.11+
- Node.js 22.16+
- PostgreSQL 18
- uv包管理器

### 后端安装
```bash
# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env
# 编辑.env文件，配置数据库连接和AI API密钥

# 运行数据库迁移
uv run alembic upgrade head

# 启动开发服务器
uv run uvicorn app.main:app --reload
```

### 前端安装（待实现）
```bash
cd frontend
npm install
npm run dev
```

### Docker部署
```bash
# 构建并启动服务
docker-compose up --build
```

## 开发指南

### API文档
启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 数据库迁移
```bash
# 创建新迁移
uv run alembic revision --autogenerate -m "description"

# 应用迁移
uv run alembic upgrade head

# 回滚迁移
uv run alembic downgrade -1
```

### 代码质量
```bash
# 代码格式化
uv run black .

# 代码检查
uv run ruff check --fix

# 类型检查
uv run mypy .
```

## 配置说明

### 环境变量
参考`.env.example`文件配置：
- `DATABASE_URL`: PostgreSQL连接字符串
- `SECRET_KEY`: JWT密钥
- `AI_PROVIDER_API_KEY`: AI服务API密钥
- `AI_MODEL`: AI模型名称

### AI功能约束
- 仅支持文本聊天，无文件上传
- 数据库查询为只读模式
- 支持自定义MCP服务器扩展

## 贡献指南

1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证。详见LICENSE文件。

## 联系方式

如有问题或建议，请通过项目issue进行反馈。