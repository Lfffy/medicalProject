#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医疗疾病数据分析系统 - 数据同步服务
创建时间：2025-06-18
功能：实现数据同步和更新功能的核心服务
"""

import threading
import time
import json
import logging
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib

from realtime_data_updater import DatabaseConfig, RealtimeDataUpdater
from data_adapters import AdapterFactory, DataSchemaManager

logger = logging.getLogger(__name__)

@dataclass
class SyncTask:
    """同步任务"""
    id: str
    source_type: str
    source_path: str
    target_table: str
    schema_name: str
    priority: int = 1
    retry_count: int = 0
    max_retries: int = 3
    last_sync_time: Optional[datetime] = None
    next_sync_time: Optional[datetime] = None
    status: str = "pending"  # pending, running, completed, failed
    error_message: Optional[str] = None
    sync_interval: int = 300  # 同步间隔（秒）

@dataclass
class SyncResult:
    """同步结果"""
    task_id: str
    status: str
    records_processed: int
    records_inserted: int
    records_updated: int
    records_failed: int
    start_time: datetime
    end_time: datetime
    error_message: Optional[str] = None

class DataSyncService:
    """数据同步服务"""
    
    def __init__(self, config_file: str = "database_config.json"):
        config_obj = DatabaseConfig(config_file)
        self.config = config_obj.config
        self.schema_manager = DataSchemaManager()
        self.updater = RealtimeDataUpdater(config_obj)
        
        self.sync_tasks: Dict[str, SyncTask] = {}
        self.sync_history: List[SyncResult] = []
        self.is_running = False
        self.sync_thread = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # 同步状态回调
        self.status_callbacks: List[Callable] = []
        
        # 加载同步任务
        self._load_sync_tasks()
    
    def _load_sync_tasks(self):
        """加载同步任务"""
        try:
            tasks_file = "sync_tasks.json"
            if os.path.exists(tasks_file):
                with open(tasks_file, 'r', encoding='utf-8') as f:
                    tasks_data = json.load(f)
                
                for task_data in tasks_data:
                    task = SyncTask(**task_data)
                    # 转换字符串时间为datetime对象
                    if task.last_sync_time:
                        task.last_sync_time = datetime.fromisoformat(task.last_sync_time)
                    if task.next_sync_time:
                        task.next_sync_time = datetime.fromisoformat(task.next_sync_time)
                    
                    self.sync_tasks[task.id] = task
                
                logger.info(f"加载了 {len(self.sync_tasks)} 个同步任务")
        except Exception as e:
            logger.error(f"加载同步任务失败：{e}")
    
    def _save_sync_tasks(self):
        """保存同步任务"""
        try:
            tasks_file = "sync_tasks.json"
            tasks_data = []
            
            for task in self.sync_tasks.values():
                task_dict = asdict(task)
                # 转换datetime对象为字符串
                if task_dict['last_sync_time']:
                    task_dict['last_sync_time'] = task.last_sync_time.isoformat()
                if task_dict['next_sync_time']:
                    task_dict['next_sync_time'] = task.next_sync_time.isoformat()
                
                tasks_data.append(task_dict)
            
            with open(tasks_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"保存同步任务失败：{e}")
    
    def add_sync_task(self, task: SyncTask) -> bool:
        """添加同步任务"""
        try:
            # 验证任务参数
            if not self._validate_task(task):
                return False
            
            # 设置下次同步时间
            if not task.next_sync_time:
                task.next_sync_time = datetime.now()
            
            self.sync_tasks[task.id] = task
            self._save_sync_tasks()
            
            logger.info(f"添加同步任务：{task.id}")
            return True
            
        except Exception as e:
            logger.error(f"添加同步任务失败：{e}")
            return False
    
    def _validate_task(self, task: SyncTask) -> bool:
        """验证同步任务"""
        try:
            # 检查适配器类型
            supported_types = AdapterFactory.get_supported_types()
            if task.source_type not in supported_types:
                logger.error(f"不支持的数据源类型：{task.source_type}")
                return False
            
            # 检查数据模式
            schema = self.schema_manager.get_schema(task.schema_name)
            if not schema:
                logger.error(f"未找到数据模式：{task.schema_name}")
                return False
            
            # 检查源路径
            if task.source_type in ['json', 'csv', 'xml']:
                if not os.path.exists(task.source_path):
                    logger.error(f"数据源文件不存在：{task.source_path}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"验证同步任务失败：{e}")
            return False
    
    def remove_sync_task(self, task_id: str) -> bool:
        """移除同步任务"""
        try:
            if task_id in self.sync_tasks:
                del self.sync_tasks[task_id]
                self._save_sync_tasks()
                logger.info(f"移除同步任务：{task_id}")
                return True
            else:
                logger.warning(f"同步任务不存在：{task_id}")
                return False
        except Exception as e:
            logger.error(f"移除同步任务失败：{e}")
            return False
    
    def start_sync_service(self):
        """启动同步服务"""
        if self.is_running:
            logger.warning("同步服务已在运行")
            return
        
        self.is_running = True
        self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.sync_thread.start()
        
        logger.info("数据同步服务已启动")
    
    def stop_sync_service(self):
        """停止同步服务"""
        self.is_running = False
        if self.sync_thread:
            self.sync_thread.join(timeout=10)
        
        self.executor.shutdown(wait=True)
        logger.info("数据同步服务已停止")
    
    def _sync_loop(self):
        """同步主循环"""
        while self.is_running:
            try:
                # 获取需要执行的任务
                current_time = datetime.now()
                tasks_to_run = []
                
                for task in self.sync_tasks.values():
                    if (task.status in ["pending", "completed", "failed"] and
                        task.next_sync_time and
                        current_time >= task.next_sync_time):
                        tasks_to_run.append(task)
                
                # 按优先级排序
                tasks_to_run.sort(key=lambda x: x.priority, reverse=True)
                
                # 执行同步任务
                for task in tasks_to_run:
                    if not self.is_running:
                        break
                    
                    # 异步执行任务
                    future = self.executor.submit(self._execute_sync_task, task)
                    future.add_done_callback(lambda f: self._handle_task_completion(f, task))
                
                # 等待一段时间再检查
                time.sleep(10)
                
            except Exception as e:
                logger.error(f"同步循环异常：{e}")
                time.sleep(30)
    
    def _execute_sync_task(self, task: SyncTask) -> SyncResult:
        """执行同步任务"""
        start_time = datetime.now()
        task.status = "running"
        task.last_sync_time = start_time
        
        # 通知状态变化
        self._notify_status_change(task)
        
        try:
            # 创建适配器
            adapter = AdapterFactory.create_adapter(task.source_type)
            
            # 读取数据
            logger.info(f"开始执行同步任务：{task.id}")
            data = adapter.read_data(task.source_path)
            
            if not data:
                raise Exception("未读取到任何数据")
            
            # 获取数据模式
            schema = self.schema_manager.get_schema(task.schema_name)
            if not schema:
                raise Exception(f"未找到数据模式：{task.schema_name}")
            
            # 转换数据
            transformed_data = adapter.transform_data(data, schema)
            
            # 同步到数据库
            result = self._sync_to_database(task.target_table, transformed_data, schema)
            
            # 更新任务状态
            end_time = datetime.now()
            task.status = "completed"
            task.next_sync_time = end_time + timedelta(seconds=task.sync_interval)
            task.retry_count = 0
            task.error_message = None
            
            sync_result = SyncResult(
                task_id=task.id,
                status="completed",
                records_processed=len(transformed_data),
                records_inserted=result.get('inserted', 0),
                records_updated=result.get('updated', 0),
                records_failed=result.get('failed', 0),
                start_time=start_time,
                end_time=end_time
            )
            
            logger.info(f"同步任务完成：{task.id}, 处理 {len(transformed_data)} 条记录")
            
        except Exception as e:
            end_time = datetime.now()
            task.status = "failed"
            task.error_message = str(e)
            task.retry_count += 1
            
            # 重试逻辑
            if task.retry_count < task.max_retries:
                # 指数退避重试
                retry_delay = min(300 * (2 ** task.retry_count), 3600)  # 最大1小时
                task.next_sync_time = end_time + timedelta(seconds=retry_delay)
                logger.warning(f"同步任务失败，将在 {retry_delay} 秒后重试：{task.id}, 错误：{e}")
            else:
                task.next_sync_time = None  # 停止重试
                logger.error(f"同步任务失败，已达到最大重试次数：{task.id}, 错误：{e}")
            
            sync_result = SyncResult(
                task_id=task.id,
                status="failed",
                records_processed=0,
                records_inserted=0,
                records_updated=0,
                records_failed=0,
                start_time=start_time,
                end_time=end_time,
                error_message=str(e)
            )
        
        # 保存任务状态
        self._save_sync_tasks()
        
        # 添加到历史记录
        self.sync_history.append(sync_result)
        
        # 限制历史记录数量
        if len(self.sync_history) > 1000:
            self.sync_history = self.sync_history[-500:]
        
        # 通知状态变化
        self._notify_status_change(task)
        
        return sync_result
    
    def _sync_to_database(self, table_name: str, data: List[Dict], schema: Dict) -> Dict:
        """同步数据到数据库"""
        try:
            db_path = self.config["database"]["path"]
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            inserted_count = 0
            updated_count = 0
            failed_count = 0
            
            for record in data:
                try:
                    # 检查记录是否已存在
                    if 'id' in record and record['id']:
                        cursor.execute(f"SELECT id FROM {table_name} WHERE id = ?", (record['id'],))
                        existing_record = cursor.fetchone()
                        
                        if existing_record:
                            # 更新现有记录
                            update_fields = [k for k in record.keys() if k != 'id']
                            if update_fields:
                                set_clause = ", ".join([f"{field} = ?" for field in update_fields])
                                values = [record[field] for field in update_fields]
                                values.append(record['id'])
                                
                                cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE id = ?", values)
                                updated_count += 1
                        else:
                            # 插入新记录
                            fields = list(record.keys())
                            placeholders = ", ".join(["?" for _ in fields])
                            values = list(record.values())
                            
                            cursor.execute(f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})", values)
                            inserted_count += 1
                    else:
                        # 没有ID，直接插入
                        fields = list(record.keys())
                        placeholders = ", ".join(["?" for _ in fields])
                        values = list(record.values())
                        
                        cursor.execute(f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})", values)
                        inserted_count += 1
                
                except Exception as e:
                    logger.error(f"同步记录失败：{e}, 记录：{record}")
                    failed_count += 1
            
            conn.commit()
            conn.close()
            
            return {
                'inserted': inserted_count,
                'updated': updated_count,
                'failed': failed_count
            }
            
        except Exception as e:
            logger.error(f"同步到数据库失败：{e}")
            raise
    
    def _handle_task_completion(self, future, task: SyncTask):
        """处理任务完成"""
        try:
            result = future.result()
            logger.info(f"任务执行完成：{task.id}, 状态：{result.status}")
        except Exception as e:
            logger.error(f"任务执行异常：{task.id}, 错误：{e}")
    
    def _notify_status_change(self, task: SyncTask):
        """通知状态变化"""
        for callback in self.status_callbacks:
            try:
                callback(task)
            except Exception as e:
                logger.error(f"状态回调执行失败：{e}")
    
    def add_status_callback(self, callback: Callable):
        """添加状态回调"""
        self.status_callbacks.append(callback)
    
    def get_sync_status(self) -> Dict:
        """获取同步状态"""
        current_time = datetime.now()
        
        status = {
            'service_running': self.is_running,
            'total_tasks': len(self.sync_tasks),
            'running_tasks': len([t for t in self.sync_tasks.values() if t.status == "running"]),
            'pending_tasks': len([t for t in self.sync_tasks.values() if t.status == "pending"]),
            'completed_tasks': len([t for t in self.sync_tasks.values() if t.status == "completed"]),
            'failed_tasks': len([t for t in self.sync_tasks.values() if t.status == "failed"]),
            'next_run_time': None,
            'recent_results': []
        }
        
        # 计算下次运行时间
        next_times = [t.next_sync_time for t in self.sync_tasks.values() if t.next_sync_time and t.next_sync_time > current_time]
        if next_times:
            status['next_run_time'] = min(next_times).isoformat()
        
        # 最近的结果
        status['recent_results'] = [
            {
                'task_id': r.task_id,
                'status': r.status,
                'records_processed': r.records_processed,
                'start_time': r.start_time.isoformat(),
                'end_time': r.end_time.isoformat(),
                'error_message': r.error_message
            }
            for r in self.sync_history[-10:]
        ]
        
        return status
    
    def get_task_list(self) -> List[Dict]:
        """获取任务列表"""
        return [
            {
                'id': task.id,
                'source_type': task.source_type,
                'source_path': task.source_path,
                'target_table': task.target_table,
                'schema_name': task.schema_name,
                'priority': task.priority,
                'status': task.status,
                'retry_count': task.retry_count,
                'max_retries': task.max_retries,
                'last_sync_time': task.last_sync_time.isoformat() if task.last_sync_time else None,
                'next_sync_time': task.next_sync_time.isoformat() if task.next_sync_time else None,
                'sync_interval': task.sync_interval,
                'error_message': task.error_message
            }
            for task in self.sync_tasks.values()
        ]
    
    def trigger_sync_task(self, task_id: str) -> bool:
        """手动触发同步任务"""
        if task_id in self.sync_tasks:
            task = self.sync_tasks[task_id]
            task.next_sync_time = datetime.now()
            task.status = "pending"
            self._save_sync_tasks()
            logger.info(f"手动触发同步任务：{task_id}")
            return True
        else:
            logger.warning(f"同步任务不存在：{task_id}")
            return False
    
    def get_sync_statistics(self) -> Dict:
        """获取同步统计信息"""
        if not self.sync_history:
            return {
                'total_syncs': 0,
                'successful_syncs': 0,
                'failed_syncs': 0,
                'total_records_processed': 0,
                'average_sync_time': 0,
                'last_24h_syncs': 0
            }
        
        total_syncs = len(self.sync_history)
        successful_syncs = len([r for r in self.sync_history if r.status == "completed"])
        failed_syncs = len([r for r in self.sync_history if r.status == "failed"])
        total_records_processed = sum(r.records_processed for r in self.sync_history)
        
        # 计算平均同步时间
        sync_times = [(r.end_time - r.start_time).total_seconds() for r in self.sync_history if r.status == "completed"]
        average_sync_time = sum(sync_times) / len(sync_times) if sync_times else 0
        
        # 最近24小时的同步次数
        last_24h = datetime.now() - timedelta(hours=24)
        last_24h_syncs = len([r for r in self.sync_history if r.start_time >= last_24h])
        
        return {
            'total_syncs': total_syncs,
            'successful_syncs': successful_syncs,
            'failed_syncs': failed_syncs,
            'total_records_processed': total_records_processed,
            'average_sync_time': average_sync_time,
            'last_24h_syncs': last_24h_syncs,
            'success_rate': (successful_syncs / total_syncs * 100) if total_syncs > 0 else 0
        }

# 使用示例
if __name__ == "__main__":
    # 创建同步服务
    sync_service = DataSyncService()
    
    # 添加示例同步任务
    task = SyncTask(
        id="medical_records_sync",
        source_type="json",
        source_path="data/medical_records.json",
        target_table="medical_records",
        schema_name="medical_records",
        priority=1,
        sync_interval=300  # 5分钟
    )
    
    sync_service.add_sync_task(task)
    
    # 启动同步服务
    sync_service.start_sync_service()
    
    try:
        # 保持服务运行
        while True:
            time.sleep(60)
            status = sync_service.get_sync_status()
            print(f"同步状态：{status}")
    except KeyboardInterrupt:
        print("停止同步服务...")
        sync_service.stop_sync_service()