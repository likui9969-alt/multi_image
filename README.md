# AI Style Studio - AI 图片风格转换平台

一个基于 FastAPI + Vue3 的企业级 AI 图片风格转换平台，支持多种艺术风格转换，提供精美 UI 和完善的用户体验。

## ✨ 功能特性

### 🎨 风格转换
- **动漫风格 (Anime)** - 将照片转换为日系动漫风格
- **油画风格 (Oil Painting)** - 经典油画艺术效果
- **素描风格 (Sketch)** - 铅笔素描效果
- **水彩风格 (Watercolor)** - 清新水彩画效果
- **像素风格 (Pixel Art)** - 复古像素艺术风格

### 👤 用户功能
- 用户注册与登录
- JWT Token 认证
- 密码显示/隐藏切换
- 登录状态持久化

### 📁 历史记录
- 转换记录列表查看
- 网格/列表视图切换
- 按风格、状态、时间筛选
- 批量删除功能
- 图片预览和下载

### 🎯 交互体验
- 企业级左右分栏登录页面
- 滑块对比原图与结果
- 实时转换进度条
- Toast 消息提示
- 确认弹窗
- 深色模式支持
- 响应式设计适配移动端

### 📊 数据统计
- 总转换数统计
- 成功率统计
- 最常用风格分析

## 🛠️ 技术栈

### 后端
- **框架**: FastAPI 0.110+
- **数据库**: SQLAlchemy 2.0 + SQLite (开发) / PostgreSQL (生产)
- **认证**: JWT (PyJWT)
- **AI 服务**: Stability AI API (SD3 Image-to-Image)
- **部署**: Uvicorn + Docker

### 前端
- **框架**: Vue 3 (Composition API)
- **路由**: Vue Router 4
- **状态管理**: Pinia（用于认证状态管理，见 `src/services/auth.js`）
- **HTTP 客户端**: Axios（封装重试 + 指数退避，见 `src/services/api.js`）
- **构建工具**: Vite 5
- **样式**: CSS3 + CSS Variables
- **字体**: Google Fonts (Inter + Poppins)

### 部署
- Docker + Docker Compose

## 📦 快速开始

### 环境要求
- Python 3.10+
- Node.js 18+
- npm 9+

### 本地开发

#### 1. 安装依赖

```bash
# 后端
cd backend
pip install -r requirements.txt

# 前端
cd frontend
npm install
```

#### 2. 启动服务

```bash
# 启动后端 (终端1)
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 启动前端 (终端2)
cd frontend
npm run dev
```

#### 3. 访问应用

- **前端**: http://localhost:3000
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

### Docker 部署

#### 环境要求
- Docker 20.10+
- Docker Compose 2.0+

#### 1. 配置环境变量

项目根目录下已包含 `.env` 文件，可根据需要修改：

```env
# 应用配置
APP_NAME=AI Style Studio
APP_HOST=0.0.0.0
APP_PORT=8000

# 数据库配置
DATABASE_URL=sqlite:///./data/style_transfer.db

# JWT 配置
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 文件上传配置
UPLOAD_DIR=./uploads
RESULT_DIR=./results
MAX_UPLOAD_SIZE_MB=10

# Stability AI 配置
STABILITY_API_KEY=*** seconds
USE_MOCK_AI=false
```

#### 2. 构建并启动容器

```bash
# 构建并启动（首次或修改代码后）
docker-compose up -d --build

# 启动已构建的容器
docker-compose up -d

# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

#### 3. 访问应用

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost:3000 |
| 后端 API | http://localhost:8000 |
| API 文档 | http://localhost:8000/docs |
| 前端健康检查 | http://localhost:3000/health |

#### 4. 停止服务

```bash
# 停止容器（保留数据）
docker-compose down

# 停止并删除数据卷（谨慎使用）
docker-compose down -v

# 停止并删除镜像（谨慎使用）
docker-compose down --rmi all
```

#### 5. Docker 配置说明

**项目结构**：
```
agent_image/
├── .env                    # 环境变量配置
├── docker-compose.yml      # Docker Compose 配置
├── backend/
│   ├── Dockerfile          # 后端 Dockerfile
│   └── ...
└── frontend/
    ├── Dockerfile          # 前端 Dockerfile
    └── nginx.conf          # Nginx 反向代理配置
```

**Docker Compose 服务**：

| 服务 | 端口 | 说明 |
|------|------|------|
| backend | 8000 | FastAPI 后端服务 |
| frontend | 3000 | Vue3 前端（Nginx 托管） |

**数据持久化**：

使用 Docker 卷进行数据持久化，即使删除容器，数据也会保留：

| 卷名 | 挂载路径 | 用途 |
|------|----------|------|
| backend_data | /app/data | SQLite 数据库 |
| backend_uploads | /app/uploads | 用户上传的图片 |
| backend_results | /app/results | 转换结果图片 |

**健康检查**：

- 后端：检查 `/api/health` 轻量端点（不暴露 Swagger UI）
- 前端：检查 `/health` 端点是否返回 "OK"

**网络配置**：

所有服务都连接到 `app-network` 网络，容器间通过服务名通信（如前端访问 `http://backend:8000`）。

#### 6. 生产环境注意事项

1. **修改 SECRET_KEY**：在 `.env` 文件中设置一个安全的随机密钥
2. **关闭 DEBUG**：设置 `DEBUG=false`
3. **配置 HTTPS**：使用 Nginx 反向代理或负载均衡器配置 SSL
4. **限制资源**：在 `docker-compose.yml` 中添加 `deploy.resources` 限制容器资源
5. **备份数据**：定期备份 `backend_data`、`backend_uploads`、`backend_results` 卷

### 首次使用

1. 访问 http://localhost:3000/login
2. 点击"注册"创建新账户
3. 登录后进入创作页面
4. 上传图片，选择风格，点击"开始转换"
5. 等待转换完成，查看结果对比

## 📁 项目结构

```
agent_image/
├── backend/                              # FastAPI 后端
│   ├── app/
│   │   ├── api/                          # API 路由
│   │   │   ├── auth.py                   # 认证接口 (注册/登录)
│   │   │   ├── images.py                 # 图片上传接口
│   │   │   ├── tasks.py                  # 任务处理接口
│   │   │   └── history.py                # 历史记录接口
│   │   ├── models/                       # 数据库模型
│   │   │   ├── user.py                   # 用户模型
│   │   │   └── image_task.py             # 图片任务模型
│   │   ├── schemas/                      # Pydantic 数据验证
│   │   │   ├── auth.py                   # 认证请求/响应
│   │   │   └── tasks.py                  # 任务请求/响应
│   │   ├── auth.py                       # JWT 认证逻辑
│   │   ├── config.py                     # 配置管理
│   │   ├── database.py                   # 数据库连接
│   │   ├── ai_service.py                 # AI 风格转换服务
│   │   └── main.py                       # 应用入口
│   ├── uploads/                          # 上传的图片存储
│   ├── results/                          # 转换结果存储
│   ├── style_transfer.db                 # SQLite 数据库文件
│   ├── requirements.txt                  # Python 依赖
│   └── Dockerfile                        # 后端 Dockerfile
├── frontend/                             # Vue3 前端
│   ├── src/
│   │   ├── views/                        # 页面视图
│   │   │   ├── LoginView.vue             # 登录/注册页面
│   │   │   ├── HomeView.vue              # 主页 (创作)
│   │   │   ├── HistoryView.vue           # 历史记录页面
│   │   │   └── NotFoundView.vue          # 404 页面
│   │   ├── components/                   # 组件
│   │   │   ├── Toast.vue                 # Toast 消息提示
│   │   │   ├── ConfirmDialog.vue         # 确认弹窗
│   │   │   └── index.js                  # 组件导出
│   │   ├── services/                     # 服务层
│   │   │   ├── api.js                    # HTTP 请求封装
│   │   │   └── auth.js                   # 认证状态管理
│   │   ├── router/                       # 路由配置
│   │   │   └── index.js                  # 路由定义
│   │   ├── styles/                       # 全局样式
│   │   │   ├── variables.css             # CSS 变量
│   │   │   └── common.css                # 公共样式
│   │   ├── App.vue                       # 根组件
│   │   └── main.js                       # 应用入口
│   ├── index.html                        # HTML 模板
│   ├── package.json                      # npm 依赖
│   ├── vite.config.js                    # Vite 配置
│   └── Dockerfile                        # 前端 Dockerfile
├── docker-compose.yml                    # Docker Compose 配置
└── README.md                             # 项目说明文档
```

## 🔌 API 接口文档

### 认证接口

#### 用户注册
```
POST /api/auth/register
```
**请求体**:
```json
{
  "username": "string (用户名)",
  "email": "string (邮箱地址)",
  "password": "string (密码，至少6位)"
}
```

#### 用户登录
```
POST /api/auth/login
```
**请求体**:
```json
{
  "email": "string (邮箱地址)",
  "password": "string (密码)"
}
```
**响应**:
```json
{
  "access_token": "string (JWT Token)",
  "token_type": "bearer",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string"
  }
}
```

### 图片接口

#### 上传图片
```
POST /api/images/upload
```
**请求头**: `Authorization: Bearer <token>`
**请求体**: `multipart/form-data`
- `file`: 图片文件 (jpg/jpeg/png/webp，最大10MB)

**响应**:
```json
{
  "task_id": 1,
  "file_path": "uploads/xxxx.png",
  "url": "/uploads/xxxx.png",
  "filename": "原始文件名.png",
  "stored_filename": "xxxx.png",
  "size": 12345,
  "status": "uploaded"
}
```

#### 提交转换任务
```
POST /api/process
```
**请求头**: `Authorization: Bearer <token>`
**请求体**:
```json
{
  "task_id": 1,
  "style_type": "anime"
}
```
**响应**:
```json
{
  "id": 1,
  "status": "completed",
  "result_image_path": "results/1_anime.jpg",
  "style_type": "anime",
  "error_message": null,
  "created_at": "2026-06-21T00:00:00",
  "updated_at": "2026-06-21T00:00:05"
}
```

### 任务接口

#### 查询任务状态
```
GET /api/tasks/{task_id}
```
**响应**:
```json
{
  "task_id": "string",
  "status": "string (uploaded/processing/completed/failed)",
  "result_image_path": "string (结果路径，完成时返回)",
  "error_message": "string (错误信息，失败时返回)"
}
```

### 历史记录接口

#### 获取历史记录
```
GET /api/history
```
**请求头**: `Authorization: Bearer <token>`
**响应**:
```json
{
  "tasks": [
    {
      "id": "integer",
      "original_filename": "string",
      "style_type": "string",
      "status": "string",
      "result_image_path": "string",
      "created_at": "string (时间戳)",
      "completed_at": "string (时间戳)"
    }
  ]
}
```

#### 删除历史记录
```
DELETE /api/history/{task_id}
```
**请求头**: `Authorization: Bearer <token>`

## ⚙️ 配置说明

### 后端配置 (.env)

```env
# 应用配置
APP_NAME=AI Style Studio
APP_HOST=0.0.0.0
APP_PORT=8000

# 数据库配置
DATABASE_URL=sqlite:///./style_transfer.db
# DATABASE_URL=postgresql://user:password@localhost/dbname

# JWT 配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 文件上传配置
UPLOAD_DIR=./uploads
RESULT_DIR=./results
MAX_UPLOAD_SIZE_MB=10

# CORS 配置（逗号分隔；生产环境请改为实际域名）
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# 文件清理（TTL，单位：小时；0 表示不清理）
FILE_TTL_HOURS=72

# 图片处理
MAX_IMAGE_DIMENSION=2048
JPEG_QUALITY=85

# AI 服务配置
# 推荐使用 OpenAI DALL-E（获取地址：https://platform.openai.com/api-keys）
AI_API_KEY=your-openai-api-key-here
AI_API_BASE_URL=https://api.openai.com/v1/images/edits
AI_TIMEOUT_SECONDS=60
# true: 使用模拟模式（Pillow 本地滤镜，无需 API key）
# false: 使用真实 AI API
USE_MOCK_AI=true
```

### 前端配置 (vite.config.js)

```javascript
export default {
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/uploads': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/results': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
}
```

## 🎨 支持的风格

| 风格 ID | 名称 | 描述 |
|---------|------|------|
| `anime` | 动漫风格 | 将照片转换为精美的日系动漫风格 |
| `oil_painting` | 油画风格 | 经典油画艺术效果，笔触细腻 |
| `sketch` | 素描风格 | 铅笔素描效果，黑白对比鲜明 |
| `watercolor` | 水彩风格 | 清新水彩画效果，色彩柔和 |
| `pixel_art` | 像素风格 | 复古像素艺术风格，8-bit 风格 |

## 📝 使用示例

### 使用 curl 测试 API

```bash
# 注册用户
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"123456"}'

# 登录获取 Token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"123456"}'

# 上传图片
curl -X POST http://localhost:8000/api/images/upload \
  -F "file=@/path/to/image.jpg"

# 提交转换任务
curl -X POST http://localhost:8000/api/process \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"file_path":"/uploads/image.jpg","style_type":"anime"}'

# 查询任务状态
curl http://localhost:8000/api/tasks/<task-id>

# 获取历史记录
curl http://localhost:8000/api/history \
  -H "Authorization: Bearer <your-token>"
```

## Stability AI

API Key: https://platform.stability.ai/account/keys

Free: 25 credits (125 images). 1 credit = 5 SD3 generations.

Set in .env: STABILITY_API_KEY=sk-... and USE_MOCK_AI=false.

## 🐛 常见问题

### Q: 前端无法访问后端 API？
A: 请确保后端服务已启动，并且前端的代理配置正确。检查 `vite.config.js` 中的 proxy 配置。

### Q: 图片上传失败？
A: 检查图片格式是否为 jpg/jpeg/png/webp，大小是否超过 10MB。

### Q: 转换任务一直显示处理中？
A: 检查 `STABILITY_API_KEY` 是否正确配置。设置 `USE_MOCK_AI=true` 可用本地滤镜测试。真实 API 超时时间在 `AI_``` (30合秒) 可调整。

### Q: 如何开启深色模式？
A: 登录后点击导航栏右侧的 🌙/☀️ 图标切换。

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**AI Style Studio** - 让创作更简单 🎨