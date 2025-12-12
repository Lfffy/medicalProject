# 孕产妇可视化智能管理平台

## 1. 项目概述

### 1.1 项目背景

随着医疗信息化的发展，孕产妇健康管理面临着数据量大、复杂度高、预测分析需求强烈等挑战。传统的孕产妇管理方式难以满足现代医疗对精准化、智能化、可视化的需求。本项目旨在构建一个集数据管理、智能分析、风险预测和可视化展示于一体的综合性平台，以提升孕产妇健康管理的效率和质量。

### 1.2 项目目标

- 提供全面的孕产妇健康数据管理功能
- 实现基于机器学习的风险预测模型，提前预警潜在健康风险
- 开发直观的数据可视化界面，支持医疗决策
- 构建实时监控系统，支持异常情况的及时预警
- 整合AI智能助手，提供医疗咨询和辅助诊断服务

### 1.3 主要功能特点

- **多维度风险预测**：支持妊娠期糖尿病、子痫前期、早产等多种风险预测
- **双模式预测机制**：结合机器学习和规则引擎，确保预测的准确性和可靠性
- **实时数据监控**：支持关键指标的实时监测和异常预警
- **数据可视化展示**：通过图表、大屏等多种形式直观展示分析结果
- **AI辅助决策**：集成智能问答系统，提供医疗咨询支持
- **权限管理**：完善的用户权限体系，确保数据安全

## 2. 系统架构

### 2.1 整体架构

系统采用前后端分离的架构设计，主要分为以下几层：

- **前端展示层**：基于Vue.js构建的SPA应用，负责用户界面展示和交互
- **后端服务层**：基于Flask的RESTful API服务，提供数据处理和业务逻辑
- **数据存储层**：采用SQLite作为轻量级数据库，存储用户数据和医疗信息
- **算法服务层**：包含机器学习模型和规则引擎，提供风险预测功能
- **实时通信层**：基于Socket.IO实现前端和后端的实时数据交互

### 2.2 技术栈

| 分类 | 技术/框架 | 版本 | 用途 |
| :--- | :--- | :--- | :--- |
| **前端** | Vue.js | 2.6.11 | 前端框架 |
| | Vue Router | 3.2.0 | 前端路由 |
| | Vuex | 3.4.0 | 状态管理 |
| | Element UI | 2.15.14 | UI组件库 |
| | ECharts | 5.4.0 | 数据可视化 |
| | DataV | 2.10.0 | 数据可视化组件 |
| | Socket.IO Client | 4.8.1 | 实时通信客户端 |
| **后端** | Python | 3.7+ | 开发语言 |
| | Flask | 最新版 | Web框架 |
| | Flask-SocketIO | 最新版 | 实时通信服务端 |
| | SQLAlchemy | 最新版 | ORM框架 |
| | pandas | 最新版 | 数据分析 |
| | numpy | 最新版 | 科学计算 |
| | scikit-learn | 最新版 | 机器学习 |
| **数据库** | SQLite | 最新版 | 数据存储 |
| **开发工具** | Git | 最新版 | 版本控制 |
| | VS Code | 最新版 | 代码编辑器 |

## 3. 核心功能模块

### 3.1 孕产妇风险预测系统

#### 3.1.1 功能概述

风险预测系统是平台的核心功能之一，通过分析孕产妇的各项生理指标和历史数据，预测潜在的健康风险。

#### 3.1.2 预测模型

系统支持三种主要的风险预测：

- **妊娠期糖尿病预测**：基于血糖水平、BMI、年龄等指标
- **子痫前期预测**：基于血压、年龄等指标
- **早产风险预测**：基于孕周、血压、既往早产史等指标

#### 3.1.3 技术实现

预测系统采用双模式架构：

- **机器学习模式**：使用预训练的分类模型进行概率预测
- **规则引擎模式**：当机器学习模型不可用时，使用专家规则进行风险评估
- **风险等级划分**：低风险(<0.4)、中风险(0.4-0.7)、高风险(≥0.7)
- **个性化建议**：根据预测结果生成针对性的健康建议

### 3.2 数据分析与可视化

#### 3.2.1 功能概述

提供强大的数据分析工具，支持多维度的数据统计和可视化展示，帮助医疗人员快速了解数据趋势和分布。

#### 3.2.2 主要功能

- **疾病分布分析**：统计各类疾病的发生率和分布情况
- **孕产妇数据分析**：分析孕期分布、风险分布等关键指标
- **趋势分析**：展示数据随时间的变化趋势
- **可视化大屏**：提供直观的数据监控大屏

#### 3.2.3 技术实现

- 使用pandas和numpy进行数据处理和统计分析
- 使用ECharts和DataV实现数据可视化
- 支持多种图表类型：柱状图、饼图、折线图、热力图等
- 支持数据导出为PDF、Excel等格式

### 3.3 实时监控系统

#### 3.3.1 功能概述

实时监控系统负责监测关键指标的变化，并在发现异常时及时发出预警。

#### 3.3.2 主要功能

- **数据更新监控**：监测数据库和文件系统的数据更新
- **指标异常预警**：当关键指标超过阈值时发出警报
- **系统性能监控**：监测系统的运行状态和性能指标
- **日志记录和分析**：记录系统运行日志，支持问题追踪

#### 3.3.3 技术实现

- 基于多线程实现后台监控任务
- 使用Socket.IO实现实时数据推送
- 支持邮件、短信等多种告警方式
- 提供监控仪表板，直观展示系统状态

### 3.4 AI智能助手

#### 3.4.1 功能概述

AI智能助手集成了大语言模型，提供智能问答、医疗咨询和辅助诊断服务。

#### 3.4.2 主要功能

- **医疗咨询问答**：回答常见的医疗问题
- **辅助诊断建议**：根据症状提供初步的诊断建议
- **用药指导**：提供基本的用药参考信息
- **健康知识普及**：提供孕产妇健康相关的知识普及

#### 3.4.3 技术实现

- 集成OpenAI API和火山方舟大模型
- 支持多模型切换和故障转移
- 实现上下文理解和多轮对话
- 支持敏感词过滤和内容审核

### 3.5 系统管理

#### 3.5.1 功能概述

系统管理模块提供用户管理、权限控制、日志查看等功能，确保系统的安全和稳定运行。

#### 3.5.2 主要功能

- **用户管理**：用户的添加、编辑、删除和权限分配
- **权限控制**：基于角色的访问控制系统
- **日志管理**：操作日志的记录和查询
- **系统配置**：全局参数的设置和管理

#### 3.5.3 技术实现

- 采用RBAC权限模型
- 实现细粒度的权限控制
- 完善的日志记录机制
- 支持配置的动态加载

## 4. 项目目录结构

```
Maternal Visualized Intelligent Management Platform/
├── data/               # 数据文件目录
│   ├── cleaned/        # 清洗后的数据
│   ├── crawled/        # 爬虫采集的数据
│   ├── test/           # 测试数据
│   └── *.json          # 各类JSON数据文件
├── front-end/          # 前端项目目录
│   ├── public/         # 静态资源
│   ├── src/            # 源代码
│   │   ├── assets/     # 资源文件
│   │   ├── components/ # Vue组件
│   │   ├── views/      # 页面视图
│   │   ├── router/     # 路由配置
│   │   └── store/      # 状态管理
│   └── package.json    # 前端依赖配置
├── models/             # 机器学习模型信息
├── spiders/            # 爬虫相关代码
├── static/             # 后端静态资源
├── templates/          # HTML模板
├── utils/              # 工具函数
├── app.py              # 后端主入口
├── maternal_risk_predictor.py # 风险预测核心模块
├── maternal_risk_api.py       # 风险预测API
├── analysis_api.py     # 数据分析API
├── monitoring_service.py # 监控服务
├── ai_chat_service.py  # AI聊天服务
├── database_setup.py   # 数据库初始化
└── requirements.txt    # Python依赖列表
```

## 5. 部署与运行

### 5.1 环境要求

- **Python**: 3.7+
- **Node.js**: 14+
- **npm**: 6+
- **Git**: 用于版本控制

### 5.2 部署步骤

#### 5.2.1 后端部署

1. 克隆代码仓库
2. 创建并激活虚拟环境
3. 安装Python依赖
4. 初始化数据库
5. 启动后端服务

```bash
# 克隆仓库
git clone https://github.com/Lfffy/medicalProject.git
cd medicalProject

# 创建虚拟环境
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python database_setup.py

# 启动服务
python app.py
```

#### 5.2.2 前端部署

1. 进入前端目录
2. 安装npm依赖
3. 启动开发服务器

```bash
cd front-end
npm install
npm run serve
```

### 5.3 生产环境部署建议

- 使用Gunicorn/uWSGI部署Flask应用
- 使用Nginx作为反向代理
- 配置HTTPS证书
- 考虑使用PostgreSQL等更强大的数据库
- 配置负载均衡和高可用性

## 6. 安全与性能

### 6.1 安全措施

- 密码加密存储
- 完善的权限控制
- 输入验证和数据清洗
- CORS配置
- 操作日志记录

### 6.2 性能优化

- 数据库索引优化
- 缓存机制
- 异步处理
- 代码优化和重构
- 负载均衡

## 7. 总结与展望

### 7.1 项目总结

孕产妇可视化智能管理平台是一个综合性的医疗管理系统，集成了数据管理、智能分析、风险预测和可视化展示等多种功能。系统采用现代化的技术架构，具有良好的扩展性和可维护性。

### 7.2 未来展望

- 进一步提升预测模型的准确性和可靠性
- 扩展更多的预测模型和分析功能
- 优化用户体验和界面设计
- 增强系统的安全性和性能
- 支持移动端访问
- 集成更多的医疗设备和数据源

## 8. 技术支持与联系方式

如有任何问题或建议，请联系项目开发团队：

- 项目邮箱：[项目支持邮箱]
- GitHub仓库：https://github.com/Lfffy/medicalProject

<img width="1827" height="871" alt="image" src="https://github.com/user-attachments/assets/0e0c61d7-d0a9-43d3-8a8a-2fe330eaaded" />
<img width="1846" height="857" alt="image" src="https://github.com/user-attachments/assets/414691d2-4d56-4a0d-8e19-b48dd39ee033" />
<img width="2046" height="1360" alt="image" src="https://github.com/user-attachments/assets/5fe8ee3f-67cb-4183-bc44-9176b69fcbcb" />
<img width="1833" height="916" alt="image" src="https://github.com/user-attachments/assets/f50c0da7-471a-4d2a-ac25-9bd8067e61da" />
<img width="1950" height="1280" alt="image" src="https://github.com/user-attachments/assets/05f0133d-6724-4128-9a27-422d17f8fb68" />
<img width="1131" height="1330" alt="image" src="https://github.com/user-attachments/assets/4832c6c1-9e9f-4c47-bdc7-db592e287ec1" />
<img width="2053" height="1334" alt="image" src="https://github.com/user-attachments/assets/cb4852df-9397-4f4c-9ca7-c607dc298703" />
<img width="1876" height="812" alt="image" src="https://github.com/user-attachments/assets/1c0dd2a1-bd0a-45fc-944d-7c4a07f9d9f4" />
<img width="1857" height="802" alt="image" src="https://github.com/user-attachments/assets/8338892d-8e0d-48be-a7c8-a2037e56b834" />
<img width="1851" height="786" alt="image" src="https://github.com/user-attachments/assets/2c7ed722-5ce5-46d3-8f9d-8c1fd1bc51ae" />
<img width="1860" height="817" alt="image" src="https://github.com/user-attachments/assets/78bed6e8-ceed-414d-81b4-209e70e1ed39" />
<img width="1825" height="761" alt="image" src="https://github.com/user-attachments/assets/4a0a030c-ef78-4daa-a164-e966887dd6d2" />
<img width="1827" height="740" alt="image" src="https://github.com/user-attachments/assets/d18c3259-462f-46dd-83ab-0dd02cfc35f2" />
<img width="1841" height="862" alt="image" src="https://github.com/user-attachments/assets/882626ba-f30d-4c18-9374-c5efe13f998e" />

孕产妇健康预测算法通过 `maternal_risk_predictor.py` 实现，采用了多种先进技术，核心特点如下：

## 1. 双模式预测机制
算法采用机器学习模型和规则引擎双模式设计，确保预测的准确性和可靠性：

- 机器学习模式 ：使用预训练模型（通过 _predict_with_ml 方法）进行概率预测
- 规则引擎模式 ：基于医学专业规则（通过 _predict_*_rules 系列方法）计算风险
- 智能降级机制 ：当机器学习模型不可用或预测失败时，自动降级到规则引擎，确保系统始终可用
## 2. 多维风险评估
系统同时评估三种关键孕期风险：

### 妊娠期糖尿病风险预测
- 核心指标 ：BMI、血糖水平、年龄
- 风险计算 ：基础风险(0.15) + BMI>28(+0.3) + 血糖>100(+0.35) + 年龄>35(+0.2)
### 子痫前期风险预测
- 核心指标 ：血压、年龄
- 风险计算 ：基础风险(0.2) + 血压>140(+0.3) + 年龄>40(+0.2)
### 早产风险预测
- 核心指标 ：孕周、血压、既往早产史
- 风险计算 ：基础风险(0.1) + 孕周<24(+0.3) + 血压>140(+0.2) + 既往早产史(+0.3)
## 3. 综合风险计算
综合风险预测通过以下步骤实现：

1. 分别预测三种风险的概率值
2. 计算三种风险的平均值作为综合风险评分
3. 应用范围限制： overall_risk = min(0.95, max(0.05, overall_risk)) ，避免极端值
4. 风险等级划分：<0.4(低风险)、0.4-0.7(中风险)、≥0.7(高风险)
5. 风险因素合并与去重，按重要性排序（最多保留5个）
## 4. 个性化建议系统
系统通过 get_comprehensive_recommendations 方法生成个性化健康建议：

- 基于风险等级提供不同频率的产检建议
- 根据患者具体健康指标（血压、BMI、血糖等）提供针对性建议
- 考虑孕周、年龄等因素提供特殊注意事项
- 限制建议数量（最多10条），避免信息过载
