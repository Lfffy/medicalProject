# 孕产妇可视化智能管理平台

## 项目介绍
本项目是一个基于Python和Vue.js开发的孕产妇可视化智能管理平台，旨在提供全面的医疗数据分析、可视化和智能预测功能，为医疗机构的孕产妇管理工作提供技术支持。

## 主要功能

### 后端功能
- 数据管理API：支持医疗数据、孕产妇信息等的增删改查操作
- 数据分析API：提供数据统计和分析功能
- 监控服务：实时监控系统状态和数据更新
- AI聊天服务：提供智能问答和辅助决策功能
- 机器学习预测：支持疾病分类、生命体征预测和患者聚类分析

### 前端功能
- 医疗数据可视化展示
- 医院管理系统界面
- 用户权限管理
- 操作日志记录
- 机器学习预测中心

## 技术栈

### 后端
- Python 3.12
- Flask Web框架
- SQLite数据库
- TensorFlow和XGBoost机器学习框架
- Socket.IO实时通信

### 前端
- Vue 2.6
- Element UI组件库
- ECharts可视化库
- Socket.IO客户端

## 快速开始

### 后端部署
1. 安装Python依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 启动后端服务：
   ```bash
   python app.py
   ```
   服务将在 http://localhost:8081 启动

### 前端部署
1. 进入前端目录：
   ```bash
   cd front-end-template-1-master
   ```

2. 安装npm依赖：
   ```bash
   npm install
   ```

3. 启动前端服务：
   ```bash
   npm run serve
   ```
   前端服务将在 http://localhost:8080 启动

## 数据库说明
- 系统使用SQLite数据库
- 数据库表结构详见 `数据库完整文档.md`
- 初始化数据可通过 `database_setup.py` 脚本创建

## 注意事项
- 系统运行需要Python 3.12环境
- 机器学习功能需要安装TensorFlow和XGBoost
- 前端服务需要Node.js环境
- 建议使用虚拟环境管理Python依赖

## 许可证
本项目采用MIT许可证。