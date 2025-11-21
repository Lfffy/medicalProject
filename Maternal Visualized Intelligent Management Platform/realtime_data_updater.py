#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医疗疾病数据分析系统 - 实时数据更新服务
创建时间：2025-06-18
功能：实现数据库实时数据同步和更新
"""

import sqlite3
import os
import time
import threading
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
import schedule
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
from dataclasses import dataclass

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('realtime_update.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class DataSourceConfig:
    """数据源配置"""
    name: str
    source_type: str  # 'file', 'api', 'database', 'websocket'
    source_path: str
    update_interval: int  # 秒
    enabled: bool = True
    last_update: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3

class DatabaseConfig:
    """数据库配置管理"""
    
    def __init__(self, config_file: str = "database_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        default_config = {
            "main_database": {
                "path": "medical_analysis.db",
                "backup_path": "medical_analysis_backup.db",
                "connection_timeout": 30,
                "max_connections": 10
            },
            "data_sources": [
                {
                    "name": "medical_records",
                    "source_type": "file",
                    "source_path": "data/medical_records.json",
                    "update_interval": 60,
                    "enabled": True
                },
                {
                    "name": "vital_signs",
                    "source_type": "api",
                    "source_path": "http://localhost:8080/api/vital-signs",
                    "update_interval": 30,
                    "enabled": True
                },
                {
                    "name": "maternal_data",
                    "source_type": "file",
                    "source_path": "data/maternal_info.json",
                    "update_interval": 120,
                    "enabled": True
                }
            ],
            "update_rules": {
                "batch_size": 100,
                "conflict_resolution": "latest",  # latest, merge, manual
                "auto_backup": True,
                "backup_interval": 3600  # 1小时
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 合并默认配置和加载的配置
                    return {**default_config, **loaded_config}
            except Exception as e:
                logger.error(f"加载配置文件失败：{e}")
        
        # 保存默认配置
        self._save_config(default_config)
        return default_config
    
    def _save_config(self, config: Dict):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存配置文件失败：{e}")

class DataFileWatcher(FileSystemEventHandler):
    """文件变化监控器"""
    
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        super().__init__()
    
    def on_modified(self, event):
        if not event.is_directory:
            logger.info(f"检测到文件变化：{event.src_path}")
            self.callback(event.src_path)

class RealtimeDataUpdater:
    """实时数据更新器"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config.config
        self.db_manager = DatabaseManager(self.config["main_database"]["path"])
        self.is_running = False
        self.update_thread = None
        self.file_observer = None
        self.data_sources = self._init_data_sources()
        self.update_callbacks = {}
        
    def get_database_path(self):
        """获取数据库路径"""
        return self.config["main_database"]["path"]
        
    def _init_data_sources(self) -> Dict[str, DataSourceConfig]:
        """初始化数据源配置"""
        sources = {}
        for source_config in self.config["data_sources"]:
            sources[source_config["name"]] = DataSourceConfig(**source_config)
        return sources
    
    def register_callback(self, event_type: str, callback: Callable):
        """注册更新回调函数"""
        if event_type not in self.update_callbacks:
            self.update_callbacks[event_type] = []
        self.update_callbacks[event_type].append(callback)
    
    def _trigger_callbacks(self, event_type: str, data: Dict):
        """触发回调函数"""
        if event_type in self.update_callbacks:
            for callback in self.update_callbacks[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"执行回调函数失败：{e}")
    
    def get_database_path(self):
        """获取数据库路径"""
        return self.config["main_database"]["path"]
    
    def start_monitoring(self):
        """启动监控"""
        if not self.is_running:
            self.is_running = True
            self.start_file_watching()
            self.start_scheduled_updates()
            logger.info("实时数据更新器已启动")
    
    def stop_monitoring(self):
        """停止监控"""
        if self.is_running:
            self.is_running = False
            if self.file_observer:
                self.file_observer.stop()
                self.file_observer.join()
            logger.info("实时数据更新器已停止")
    
    def start_file_watching(self):
        """启动文件监控"""
        if not self.file_observer:
            self.file_observer = Observer()
            handler = DataFileWatcher(self._handle_file_change)
            
            # 监控数据目录
            data_dir = "data"
            if os.path.exists(data_dir):
                self.file_observer.schedule(handler, data_dir, recursive=True)
                self.file_observer.start()
                logger.info("文件监控已启动")
    
    def start_scheduled_updates(self):
        """启动定时更新"""
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time.sleep(1)
        
        # 设置定时任务
        for source_name, source_config in self.data_sources.items():
            if source_config.enabled:
                schedule.every(source_config.update_interval).seconds.do(
                    self._update_data_source, source_name
                )
        
        # 启动调度器线程
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        logger.info("定时更新已启动")
    
    def _handle_file_change(self, file_path: str):
        """处理文件变化"""
        filename = os.path.basename(file_path)
        
        # 查找对应的数据源
        for source_name, source_config in self.data_sources.items():
            if filename in source_config.source_path:
                logger.info(f"检测到数据源 {source_name} 的文件变化")
                self._update_data_source(source_name)
                break
    
    def _update_data_source(self, source_name: str):
        """更新指定数据源"""
        if source_name not in self.data_sources:
            logger.error(f"未知数据源：{source_name}")
            return
        
        source_config = self.data_sources[source_name]
        
        if not source_config.enabled:
            logger.info(f"数据源 {source_name} 已禁用，跳过更新")
            return
        
        try:
            logger.info(f"开始更新数据源：{source_name}")
            
            if source_config.source_type == "file":
                success = self._update_from_file(source_config)
            elif source_config.source_type == "api":
                success = self._update_from_api(source_config)
            elif source_config.source_type == "database":
                success = self._update_from_database(source_config)
            else:
                logger.error(f"不支持的数据源类型：{source_config.source_type}")
                return
            
            if success:
                source_config.last_update = datetime.now()
                source_config.retry_count = 0
                logger.info(f"数据源 {source_name} 更新成功")
                
                # 触发更新成功回调
                self._trigger_callbacks("update_success", {
                    "source": source_name,
                    "update_time": source_config.last_update.isoformat()
                })
            else:
                source_config.retry_count += 1
                logger.error(f"数据源 {source_name} 更新失败，重试次数：{source_config.retry_count}")
                
                if source_config.retry_count >= source_config.max_retries:
                    logger.error(f"数据源 {source_name} 达到最大重试次数，暂时禁用")
                    source_config.enabled = False
                
                # 触发更新失败回调
                self._trigger_callbacks("update_failed", {
                    "source": source_name,
                    "retry_count": source_config.retry_count,
                    "error": "更新失败"
                })
        
        except Exception as e:
            logger.error(f"更新数据源 {source_name} 时发生异常：{e}")
            source_config.retry_count += 1
    
    def _update_from_file(self, source_config: DataSourceConfig) -> bool:
        """从文件更新数据"""
        try:
            if not os.path.exists(source_config.source_path):
                logger.error(f"数据文件不存在：{source_config.source_path}")
                return False
            
            with open(source_config.source_path, 'r', encoding='utf-8') as f:
                if source_config.source_path.endswith('.json'):
                    data = json.load(f)
                else:
                    # 处理其他格式的文件
                    logger.warning(f"暂不支持的文件格式：{source_config.source_path}")
                    return False
            
            # 根据数据类型更新相应的数据库表
            return self._save_data_to_database(source_config.source_path, data)
        
        except Exception as e:
            logger.error(f"从文件更新数据失败：{e}")
            return False
    
    def _update_from_api(self, source_config: DataSourceConfig) -> bool:
        """从API更新数据"""
        try:
            response = requests.get(
                source_config.source_path,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            
            data = response.json()
            return self._save_data_to_database(source_config.source_path, data)
        
        except Exception as e:
            logger.error(f"从API更新数据失败：{e}")
            return False
    
    def _update_from_database(self, source_config: DataSourceConfig) -> bool:
        """从其他数据库更新数据"""
        # 这里可以实现从其他数据库同步数据的逻辑
        logger.info("从其他数据库同步数据功能待实现")
        return True
    
    def _save_data_to_database(self, source_path: str, data: List[Dict]) -> bool:
        """保存数据到数据库"""
        try:
            if not self.db_manager.connect():
                return False
            
            # 根据数据源路径确定目标表
            table_name = self._get_table_name_from_source(source_path)
            
            if not table_name:
                logger.error(f"无法确定数据源 {source_path} 对应的数据库表")
                return False
            
            # 批量插入或更新数据
            batch_size = self.config["update_rules"]["batch_size"]
            
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                
                for record in batch:
                    if self._record_exists(table_name, record.get('id')):
                        self._update_record(table_name, record)
                    else:
                        self._insert_record(table_name, record)
            
            logger.info(f"成功更新表 {table_name}，共处理 {len(data)} 条记录")
            return True
        
        except Exception as e:
            logger.error(f"保存数据到数据库失败：{e}")
            return False
        finally:
            self.db_manager.disconnect()
    
    def _get_table_name_from_source(self, source_path: str) -> Optional[str]:
        """根据数据源路径获取目标表名"""
        filename = os.path.basename(source_path).lower()
        
        if 'medical_record' in filename:
            return 'medical_records'
        elif 'vital_sign' in filename:
            return 'vital_signs'
        elif 'maternal' in filename:
            return 'maternal_info'
        elif 'patient' in filename:
            return 'patients'
        else:
            return None
    
    def _record_exists(self, table_name: str, record_id: Optional[int]) -> bool:
        """检查记录是否存在"""
        if not record_id:
            return False
        
        query = f"SELECT COUNT(*) as count FROM {table_name} WHERE id = ?"
        result = self.db_manager.execute_query(query, (record_id,))
        return result[0]['count'] > 0 if result else False
    
    def _insert_record(self, table_name: str, record: Dict):
        """插入记录"""
        # 移除id字段，让数据库自动生成
        if 'id' in record:
            del record['id']
        
        columns = list(record.keys())
        placeholders = ['?' for _ in columns]
        values = list(record.values())
        
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        self.db_manager.execute_query(query, values)
    
    def _update_record(self, table_name: str, record: Dict):
        """更新记录"""
        if 'id' not in record:
            return
        
        record_id = record['id']
        del record['id']
        
        columns = list(record.keys())
        values = list(record.values())
        values.append(record_id)
        
        set_clause = ', '.join([f"{col} = ?" for col in columns])
        query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
        self.db_manager.execute_query(query, values)
    
    def start_scheduled_updates(self):
        """启动定时更新"""
        for source_name, source_config in self.data_sources.items():
            if source_config.enabled:
                schedule.every(source_config.update_interval).seconds.do(
                    self._update_data_source, source_name
                )
        
        logger.info("定时更新任务已启动")
        
        # 运行调度器
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
    
    def start(self):
        """启动实时更新服务"""
        if self.is_running:
            logger.warning("实时更新服务已在运行")
            return
        
        self.is_running = True
        
        # 启动文件监控
        self.start_file_watching()
        
        # 启动定时更新线程
        self.update_thread = threading.Thread(target=self.start_scheduled_updates)
        self.update_thread.daemon = True
        self.update_thread.start()
        
        logger.info("实时数据更新服务已启动")
    
    def stop(self):
        """停止实时更新服务"""
        self.is_running = False
        
        if self.file_observer:
            self.file_observer.stop()
            self.file_observer.join()
        
        if self.update_thread:
            self.update_thread.join(timeout=5)
        
        logger.info("实时数据更新服务已停止")
    
    def get_status(self) -> Dict:
        """获取更新服务状态"""
        return {
            "is_running": self.is_running,
            "data_sources": {
                name: {
                    "enabled": config.enabled,
                    "last_update": config.last_update.isoformat() if config.last_update else None,
                    "retry_count": config.retry_count,
                    "update_interval": config.update_interval
                }
                for name, config in self.data_sources.items()
            },
            "next_updates": {
                name: schedule.next_run() if schedule.jobs else None
                for name in self.data_sources.keys()
            }
        }

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
    
    def connect(self) -> bool:
        """连接数据库"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            return True
        except Exception as e:
            logger.error(f"连接数据库失败：{e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query: str, params: tuple = None):
        """执行查询"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return [dict(row) for row in results]
            else:
                self.connection.commit()
                return cursor.rowcount
        except Exception as e:
            logger.error(f"执行查询失败：{e}")
            return None

def main():
    """主函数"""
    logger.info("启动实时数据更新服务...")
    
    # 加载配置
    config = DatabaseConfig()
    
    # 创建更新器
    updater = RealtimeDataUpdater(config)
    
    try:
        # 启动服务
        updater.start()
        
        # 保持服务运行
        while True:
            time.sleep(60)
            
            # 打印状态信息
            status = updater.get_status()
            logger.info(f"服务状态：{json.dumps(status, ensure_ascii=False, indent=2)}")
    
    except KeyboardInterrupt:
        logger.info("收到停止信号")
    finally:
        updater.stop()
        logger.info("实时数据更新服务已停止")

if __name__ == "__main__":
    main()