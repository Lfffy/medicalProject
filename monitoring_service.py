#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医疗疾病数据分析系统 - 数据更新监控和日志系统
创建时间：2025-06-18
功能：提供数据更新的监控、日志记录和告警功能
"""

import logging
import json
import os
import time
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from threading import Thread, Event
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

@dataclass
class LogEntry:
    """日志条目"""
    timestamp: datetime
    level: str  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    module: str
    message: str
    details: Optional[Dict] = None
    task_id: Optional[str] = None
    user_id: Optional[str] = None

@dataclass
class AlertRule:
    """告警规则"""
    id: str
    name: str
    description: str
    condition: str  # 告警条件表达式
    threshold: float
    time_window: int  # 时间窗口（分钟）
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    enabled: bool = True
    notification_channels: List[str] = None  # email, webhook, sms
    created_at: datetime = None
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0

@dataclass
class MetricData:
    """指标数据"""
    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str] = None
    unit: str = ""

class DatabaseHandler(logging.Handler):
    """数据库日志处理器"""
    
    def __init__(self, db_path: str):
        super().__init__()
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化日志数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    level TEXT NOT NULL,
                    module TEXT NOT NULL,
                    message TEXT NOT NULL,
                    details TEXT,
                    task_id TEXT,
                    user_id TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON system_logs(timestamp)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_logs_level ON system_logs(level)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_logs_module ON system_logs(module)
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"初始化日志数据库失败：{e}")
    
    def emit(self, record):
        """写入日志到数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 解析日志记录
            log_entry = LogEntry(
                timestamp=datetime.fromtimestamp(record.created),
                level=record.levelname,
                module=record.module,
                message=record.getMessage(),
                details=getattr(record, 'details', None),
                task_id=getattr(record, 'task_id', None),
                user_id=getattr(record, 'user_id', None)
            )
            
            cursor.execute('''
                INSERT INTO system_logs 
                (timestamp, level, module, message, details, task_id, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                log_entry.timestamp,
                log_entry.level,
                log_entry.module,
                log_entry.message,
                json.dumps(log_entry.details) if log_entry.details else None,
                log_entry.task_id,
                log_entry.user_id
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"写入日志数据库失败：{e}")

class MetricsCollector:
    """指标收集器"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.metrics_buffer = deque(maxlen=10000)
        self._init_database()
    
    def _init_database(self):
        """初始化指标数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    value REAL NOT NULL,
                    timestamp DATETIME NOT NULL,
                    tags TEXT,
                    unit TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_metrics_name_timestamp ON metrics(name, timestamp)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"初始化指标数据库失败：{e}")
    
    def record_metric(self, metric: MetricData):
        """记录指标"""
        try:
            # 添加到缓冲区
            self.metrics_buffer.append(metric)
            
            # 批量写入数据库
            if len(self.metrics_buffer) >= 100:
                self._flush_metrics()
                
        except Exception as e:
            logger.error(f"记录指标失败：{e}")
    
    def _flush_metrics(self):
        """批量写入指标到数据库"""
        if not self.metrics_buffer:
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            metrics_to_write = list(self.metrics_buffer)
            self.metrics_buffer.clear()
            
            for metric in metrics_to_write:
                cursor.execute('''
                    INSERT INTO metrics (name, value, timestamp, tags, unit)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    metric.name,
                    metric.value,
                    metric.timestamp,
                    json.dumps(metric.tags) if metric.tags else None,
                    metric.unit
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"批量写入指标失败：{e}")
    
    def get_metrics(self, name: str, start_time: datetime, end_time: datetime, 
                   tags: Dict[str, str] = None) -> List[MetricData]:
        """获取指标数据"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = '''
                SELECT name, value, timestamp, tags, unit
                FROM metrics
                WHERE name = ? AND timestamp BETWEEN ? AND ?
            '''
            params = [name, start_time, end_time]
            
            if tags:
                for key, value in tags.items():
                    query += f" AND json_extract(tags, '$.{key}') = ?"
                    params.append(value)
            
            query += " ORDER BY timestamp"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            metrics = []
            for row in rows:
                tags_dict = json.loads(row[3]) if row[3] else None
                metric = MetricData(
                    name=row[0],
                    value=row[1],
                    timestamp=datetime.fromisoformat(row[2]),
                    tags=tags_dict,
                    unit=row[4] or ""
                )
                metrics.append(metric)
            
            return metrics
            
        except Exception as e:
            logger.error(f"获取指标数据失败：{e}")
            return []
    
    def get_metric_summary(self, name: str, start_time: datetime, end_time: datetime) -> Dict:
        """获取指标汇总信息"""
        metrics = self.get_metrics(name, start_time, end_time)
        
        if not metrics:
            return {
                'count': 0,
                'min': None,
                'max': None,
                'avg': None,
                'sum': None
            }
        
        values = [m.value for m in metrics]
        return {
            'count': len(values),
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'sum': sum(values)
        }

class AlertManager:
    """告警管理器"""
    
    def __init__(self, config_file: str = "alert_config.json"):
        self.config_file = config_file
        self.rules = self._load_rules()
        self.notification_config = self._load_notification_config()
        self.metrics_collector = None
    
    def _load_rules(self) -> Dict[str, AlertRule]:
        """加载告警规则"""
        default_rules = {
            "sync_failure_rate": AlertRule(
                id="sync_failure_rate",
                name="同步失败率告警",
                description="当同步失败率超过阈值时触发告警",
                condition="failure_rate > threshold",
                threshold=10.0,
                time_window=60,
                severity="HIGH",
                notification_channels=["email", "webhook"]
            ),
            "data_processing_delay": AlertRule(
                id="data_processing_delay",
                name="数据处理延迟告警",
                description="当数据处理延迟超过阈值时触发告警",
                condition="processing_delay > threshold",
                threshold=300.0,
                time_window=30,
                severity="MEDIUM",
                notification_channels=["email"]
            ),
            "database_connection_error": AlertRule(
                id="database_connection_error",
                name="数据库连接错误告警",
                description="当数据库连接错误时触发告警",
                condition="connection_errors > threshold",
                threshold=0.0,
                time_window=5,
                severity="CRITICAL",
                notification_channels=["email", "webhook", "sms"]
            )
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    rules_data = json.load(f)
                
                for rule_data in rules_data:
                    rule = AlertRule(**rule_data)
                    if rule.created_at:
                        rule.created_at = datetime.fromisoformat(rule.created_at)
                    if rule.last_triggered:
                        rule.last_triggered = datetime.fromisoformat(rule.last_triggered)
                    
                    default_rules[rule.id] = rule
                    
            except Exception as e:
                logger.error(f"加载告警规则失败：{e}")
        
        return default_rules
    
    def _load_notification_config(self) -> Dict:
        """加载通知配置"""
        default_config = {
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "from_address": "monitor@medical-system.com",
                "to_addresses": ["admin@medical-system.com"]
            },
            "webhook": {
                "enabled": False,
                "url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
                "timeout": 30
            },
            "sms": {
                "enabled": False,
                "api_url": "https://api.sms-service.com/send",
                "api_key": "9511e57c-7838-415d-8225-fd89678c6311",
                "phone_numbers": []
            }
        }
        
        config_file = "notification_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return {**default_config, **json.load(f)}
            except Exception as e:
                logger.error(f"加载通知配置失败：{e}")
        
        return default_config
    
    def set_metrics_collector(self, metrics_collector: MetricsCollector):
        """设置指标收集器"""
        self.metrics_collector = metrics_collector
    
    def check_alerts(self):
        """检查告警条件"""
        current_time = datetime.now()
        
        for rule in self.rules.values():
            if not rule.enabled:
                continue
            
            try:
                # 评估告警条件
                if self._evaluate_rule(rule, current_time):
                    self._trigger_alert(rule)
                    
            except Exception as e:
                logger.error(f"检查告警规则失败 {rule.id}：{e}")
    
    def _evaluate_rule(self, rule: AlertRule, current_time: datetime) -> bool:
        """评估告警规则"""
        if not self.metrics_collector:
            return False
        
        # 计算时间窗口
        start_time = current_time - timedelta(minutes=rule.time_window)
        
        # 根据规则ID获取相应的指标
        if rule.id == "sync_failure_rate":
            # 计算同步失败率
            success_metrics = self.metrics_collector.get_metrics("sync_success_count", start_time, current_time)
            failure_metrics = self.metrics_collector.get_metrics("sync_failure_count", start_time, current_time)
            
            total_syncs = sum(m.value for m in success_metrics) + sum(m.value for m in failure_metrics)
            if total_syncs == 0:
                return False
            
            failure_rate = (sum(m.value for m in failure_metrics) / total_syncs) * 100
            return failure_rate > rule.threshold
            
        elif rule.id == "data_processing_delay":
            # 检查数据处理延迟
            delay_metrics = self.metrics_collector.get_metrics("processing_delay", start_time, current_time)
            if not delay_metrics:
                return False
            
            max_delay = max(m.value for m in delay_metrics)
            return max_delay > rule.threshold
            
        elif rule.id == "database_connection_error":
            # 检查数据库连接错误
            error_metrics = self.metrics_collector.get_metrics("database_connection_errors", start_time, current_time)
            if not error_metrics:
                return False
            
            total_errors = sum(m.value for m in error_metrics)
            return total_errors > rule.threshold
        
        return False
    
    def _trigger_alert(self, rule: AlertRule):
        """触发告警"""
        current_time = datetime.now()
        
        # 更新规则状态
        rule.last_triggered = current_time
        rule.trigger_count += 1
        
        # 构建告警消息
        alert_message = self._build_alert_message(rule)
        
        # 发送通知
        for channel in rule.notification_channels:
            try:
                if channel == "email":
                    self._send_email_alert(alert_message, rule)
                elif channel == "webhook":
                    self._send_webhook_alert(alert_message, rule)
                elif channel == "sms":
                    self._send_sms_alert(alert_message, rule)
                    
            except Exception as e:
                logger.error(f"发送告警通知失败 {channel}：{e}")
        
        # 记录告警日志
        logger.warning(f"触发告警：{rule.name}", extra={
            'details': {
                'rule_id': rule.id,
                'severity': rule.severity,
                'trigger_count': rule.trigger_count,
                'message': alert_message
            }
        })
    
    def _build_alert_message(self, rule: AlertRule) -> str:
        """构建告警消息"""
        return f"""
告警规则：{rule.name}
告警级别：{rule.severity}
触发时间：{rule.last_triggered}
触发次数：{rule.trigger_count}
描述：{rule.description}

请及时检查系统状态并处理相关问题。
        """.strip()
    
    def _send_email_alert(self, message: str, rule: AlertRule):
        """发送邮件告警"""
        config = self.notification_config.get("email", {})
        if not config.get("enabled"):
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = config['from_address']
            msg['To'] = ', '.join(config['to_addresses'])
            msg['Subject'] = f"[{rule.severity}] 医疗系统告警：{rule.name}"
            
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
            server.starttls()
            server.login(config['username'], config['password'])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"邮件告警发送成功：{rule.name}")
            
        except Exception as e:
            logger.error(f"发送邮件告警失败：{e}")
    
    def _send_webhook_alert(self, message: str, rule: AlertRule):
        """发送Webhook告警"""
        config = self.notification_config.get("webhook", {})
        if not config.get("enabled"):
            return
        
        try:
            payload = {
                "text": f"[{rule.severity}] 医疗系统告警：{rule.name}",
                "attachments": [
                    {
                        "color": self._get_color_by_severity(rule.severity),
                        "fields": [
                            {"title": "告警规则", "value": rule.name, "short": True},
                            {"title": "告警级别", "value": rule.severity, "short": True},
                            {"title": "触发时间", "value": rule.last_triggered.isoformat(), "short": True},
                            {"title": "描述", "value": rule.description, "short": False}
                        ]
                    }
                ]
            }
            
            response = requests.post(
                config['url'],
                json=payload,
                timeout=config.get('timeout', 30)
            )
            response.raise_for_status()
            
            logger.info(f"Webhook告警发送成功：{rule.name}")
            
        except Exception as e:
            logger.error(f"发送Webhook告警失败：{e}")
    
    def _send_sms_alert(self, message: str, rule: AlertRule):
        """发送短信告警"""
        config = self.notification_config.get("sms", {})
        if not config.get("enabled"):
            return
        
        try:
            for phone_number in config['phone_numbers']:
                payload = {
                    "api_key": config['api_key'],
                    "phone": phone_number,
                    "message": f"[{rule.severity}] {rule.name}: {rule.description}"
                }
                
                response = requests.post(config['api_url'], json=payload, timeout=30)
                response.raise_for_status()
            
            logger.info(f"短信告警发送成功：{rule.name}")
            
        except Exception as e:
            logger.error(f"发送短信告警失败：{e}")
    
    def _get_color_by_severity(self, severity: str) -> str:
        """根据严重程度获取颜色"""
        color_map = {
            "LOW": "good",
            "MEDIUM": "warning", 
            "HIGH": "danger",
            "CRITICAL": "#ff0000"
        }
        return color_map.get(severity, "warning")

class MonitoringService:
    """监控服务"""
    
    def __init__(self, config_file: str = "database_config.json"):
        self.config_file = config_file
        self.db_path = "medical_data.db"
        self.metrics_collector = MetricsCollector(f"{self.db_path.replace('.db', '_metrics.db')}")
        self.alert_manager = AlertManager()
        self.alert_manager.set_metrics_collector(self.metrics_collector)
        
        self.is_running = False
        self.monitor_thread = None
        self.stop_event = Event()
        
        # 设置日志处理器
        self._setup_logging()
    
    def _setup_logging(self):
        """设置日志系统"""
        # 创建数据库日志处理器
        db_handler = DatabaseHandler(f"{self.db_path.replace('.db', '_logs.db')}")
        db_handler.setLevel(logging.INFO)
        
        # 添加到根日志记录器
        logging.getLogger().addHandler(db_handler)
    
    def start_monitoring(self):
        """启动监控服务"""
        if self.is_running:
            logger.warning("监控服务已在运行")
            return
        
        self.is_running = True
        self.stop_event.clear()
        self.monitor_thread = Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info("监控服务已启动")
    
    def stop_monitoring(self):
        """停止监控服务"""
        self.is_running = False
        self.stop_event.set()
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=10)
        
        # 刷新指标缓冲区
        self.metrics_collector._flush_metrics()
        
        logger.info("监控服务已停止")
    
    def _monitoring_loop(self):
        """监控主循环"""
        while self.is_running and not self.stop_event.is_set():
            try:
                # 检查告警
                self.alert_manager.check_alerts()
                
                # 记录系统指标
                self._record_system_metrics()
                
                # 等待下一次检查
                if self.stop_event.wait(timeout=60):  # 每分钟检查一次
                    break
                    
            except Exception as e:
                logger.error(f"监控循环异常：{e}")
                time.sleep(30)
    
    def _record_system_metrics(self):
        """记录系统指标"""
        current_time = datetime.now()
        
        try:
            # 记录数据库连接数（模拟）
            self.metrics_collector.record_metric(MetricData(
                name="database_connections",
                value=5.0,  # 模拟值
                timestamp=current_time,
                unit="count"
            ))
            
            # 记录内存使用率（模拟）
            self.metrics_collector.record_metric(MetricData(
                name="memory_usage",
                value=65.5,  # 模拟值
                timestamp=current_time,
                unit="percent"
            ))
            
            # 记录CPU使用率（模拟）
            self.metrics_collector.record_metric(MetricData(
                name="cpu_usage",
                value=45.2,  # 模拟值
                timestamp=current_time,
                unit="percent"
            ))
            
        except Exception as e:
            logger.error(f"记录系统指标失败：{e}")
    
    def record_sync_metrics(self, task_id: str, success: bool, processing_time: float):
        """记录同步指标"""
        current_time = datetime.now()
        
        try:
            # 记录同步成功/失败次数
            metric_name = "sync_success_count" if success else "sync_failure_count"
            self.metrics_collector.record_metric(MetricData(
                name=metric_name,
                value=1.0,
                timestamp=current_time,
                tags={"task_id": task_id},
                unit="count"
            ))
            
            # 记录处理时间
            self.metrics_collector.record_metric(MetricData(
                name="processing_time",
                value=processing_time,
                timestamp=current_time,
                tags={"task_id": task_id},
                unit="seconds"
            ))
            
        except Exception as e:
            logger.error(f"记录同步指标失败：{e}")
    
    def get_monitoring_dashboard(self) -> Dict:
        """获取监控仪表板数据"""
        current_time = datetime.now()
        last_24h = current_time - timedelta(hours=24)
        
        try:
            # 获取最近24小时的指标
            cpu_metrics = self.metrics_collector.get_metrics("cpu_usage", last_24h, current_time)
            memory_metrics = self.metrics_collector.get_metrics("memory_usage", last_24h, current_time)
            sync_success = self.metrics_collector.get_metrics("sync_success_count", last_24h, current_time)
            sync_failure = self.metrics_collector.get_metrics("sync_failure_count", last_24h, current_time)
            
            # 计算汇总数据
            cpu_summary = self.metrics_collector.get_metric_summary("cpu_usage", last_24h, current_time)
            memory_summary = self.metrics_collector.get_metric_summary("memory_usage", last_24h, current_time)
            
            total_syncs = sum(m.value for m in sync_success) + sum(m.value for m in sync_failure)
            sync_success_rate = (sum(m.value for m in sync_success) / total_syncs * 100) if total_syncs > 0 else 0
            
            return {
                "system_status": {
                    "cpu_usage": cpu_summary.get('avg', 0),
                    "memory_usage": memory_summary.get('avg', 0),
                    "database_connections": 5,  # 模拟值
                },
                "sync_status": {
                    "total_syncs": int(total_syncs),
                    "success_rate": sync_success_rate,
                    "last_24h_syncs": int(total_syncs)
                },
                "alerts": {
                    "active_rules": len([r for r in self.alert_manager.rules.values() if r.enabled]),
                    "recent_triggers": len([r for r in self.alert_manager.rules.values() 
                                         if r.last_triggered and r.last_triggered > last_24h])
                },
                "timestamp": current_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"获取监控仪表板数据失败：{e}")
            return {"error": str(e)}

# 使用示例
if __name__ == "__main__":
    # 创建监控服务
    monitoring_service = MonitoringService()
    
    # 启动监控
    monitoring_service.start_monitoring()
    
    try:
        # 模拟记录一些指标
        import random
        for i in range(10):
            monitoring_service.record_sync_metrics(
                f"task_{i}",
                random.choice([True, False]),
                random.uniform(1, 10)
            )
            time.sleep(1)
        
        # 获取监控数据
        dashboard = monitoring_service.get_monitoring_dashboard()
        print(f"监控仪表板：{json.dumps(dashboard, indent=2, ensure_ascii=False)}")
        
        # 保持监控运行
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("停止监控服务...")
        monitoring_service.stop_monitoring()