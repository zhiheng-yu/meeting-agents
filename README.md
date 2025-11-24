# Meeting Agents

一个基于 Agno 框架的智能会议助手系统，提供会议转录总结和基于知识库的智能问答功能。

## 功能特性

- **会议总结代理 (Summary Agent)**: 自动分析会议转录文本，生成结构化的专业会议纪要
- **会议咨询代理 (Counselor Agent)**: 基于会议知识库，智能回答关于会议内容的问题
- **知识库管理**: 使用 PostgreSQL + pgvector 存储会议内容，支持向量搜索和混合搜索
- **RESTful API**: 通过 AgentOS 提供统一的 API 接口

## 系统架构

```
┌─────────────────┐
│   AgentOS API   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│Summary│ │Counselor│
│ Agent │ │  Agent  │
└───────┘ └────┬────┘
               │
        ┌──────▼──────┐
        │  Knowledge  │
        │    Base     │
        │ (PostgreSQL)│
        └─────────────┘
```

## 项目结构

```
meeting-agents/
├── agno_os.py          # AgentOS 主入口
├── summarizer.py       # 会议总结代理
├── counselor.py        # 会议咨询代理
├── config/             # 配置文件
│   ├── summary_prompt.md      # 总结代理提示词
│   ├── counselor_prompt.md    # 咨询代理提示词
│   └── minutes_format.md      # 会议纪要格式模板
├── sample.txt          # 示例会议转录文件
├── requirements.txt    # Python 依赖
├── Dockerfile          # Docker 镜像配置
└── docker-compose.yml  # Docker Compose 配置
```

## 环境要求

- Python 3.12+
- PostgreSQL 数据库（支持 pgvector 扩展）
- OpenAI 兼容的 API（如 OpenAI、Qwen 等）

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/zhiheng-yu/meeting-agents.git
cd meeting-agents
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件并配置以下变量：

```env
# OpenAI 兼容 API 配置
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1       # 或你的 API 服务地址
OPENAI_MODEL=gpt-4o-mini                        # 使用的模型名称
OPENAI_EMBEDDING_MODEL=text-embedding-3-small   # 嵌入模型名称

# 数据库配置
POSTGRES_DB_URL=postgresql://user:password@localhost:5432/dbname

# 调试模式（可选）
AGNO_DEBUG_MODE=False
```

### 4. 初始化数据库

确保 PostgreSQL 数据库已安装并启用 pgvector 扩展
或通过 docker 一键部署 pgvector

```bash
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  agnohq/pgvector:16
```

## 使用方法

### 方式一：直接运行 Python 脚本

#### 使用总结代理

```bash
python summarizer.py
# 然后输入会议转录文件的路径
```

#### 使用咨询代理

```bash
python counselor.py
# 代理会自动加载知识库并回答关于会议的问题
```

### 方式二：使用 AgentOS API 服务

#### 启动服务

```bash
python agno_os.py
```

服务将在 `http://localhost:7777` 启动。

#### 使用 Docker Compose

```bash
# 构建镜像
docker build -t meeting-agents .

# 启动服务
docker-compose up -d
```

## 接口使用方法

[会议Agents接口文档-Apifox](https://s.apifox.cn/15d90b10-351f-4dca-9a45-097402efc241)

## 技术栈

- [Agno](https://github.com/agno-agi/agno): AI 代理框架
- FastAPI: Web 框架
- PostgreSQL + pgvector: 向量数据库
- OpenAI API: 大语言模型和嵌入模型
