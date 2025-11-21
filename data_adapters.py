#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医疗疾病数据分析系统 - 数据源适配器
创建时间：2025-06-18
功能：实现不同数据源的适配和转换
"""

import json
import csv
import xml.etree.ElementTree as ET
import pandas as pd
import sqlite3
import requests
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class DataAdapter(ABC):
    """数据适配器抽象基类"""
    
    @abstractmethod
    def read_data(self, source_path: str, **kwargs) -> List[Dict]:
        """读取数据"""
        pass
    
    @abstractmethod
    def validate_data(self, data: List[Dict]) -> bool:
        """验证数据格式"""
        pass
    
    @abstractmethod
    def transform_data(self, data: List[Dict], target_schema: Dict) -> List[Dict]:
        """转换数据格式"""
        pass

class JSONAdapter(DataAdapter):
    """JSON数据适配器"""
    
    def read_data(self, source_path: str, **kwargs) -> List[Dict]:
        """读取JSON数据"""
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 如果是单个对象，转换为列表
            if isinstance(data, dict):
                data = [data]
            elif isinstance(data, list):
                data = data
            else:
                raise ValueError("JSON数据格式不正确，应为对象或数组")
            
            logger.info(f"成功读取JSON数据，共 {len(data)} 条记录")
            return data
        except Exception as e:
            logger.error(f"读取JSON数据失败：{e}")
            return []
    
    def validate_data(self, data: List[Dict]) -> bool:
        """验证JSON数据格式"""
        if not isinstance(data, list):
            return False
        
        for record in data:
            if not isinstance(record, dict):
                return False
        
        return True
    
    def transform_data(self, data: List[Dict], target_schema: Dict) -> List[Dict]:
        """转换JSON数据格式"""
        transformed_data = []
        
        for record in data:
            transformed_record = {}
            
            for field_name, field_config in target_schema.items():
                source_field = field_config.get('source_field', field_name)
                data_type = field_config.get('type', 'string')
                default_value = field_config.get('default', None)
                required = field_config.get('required', False)
                
                # 获取源数据
                value = record.get(source_field, default_value)
                
                # 数据类型转换
                if value is not None:
                    value = self._convert_data_type(value, data_type)
                
                # 检查必填字段
                if required and value is None:
                    logger.warning(f"必填字段 {field_name} 缺失")
                    continue
                
                transformed_record[field_name] = value
            
            transformed_data.append(transformed_record)
        
        return transformed_data
    
    def _convert_data_type(self, value: Any, target_type: str) -> Any:
        """数据类型转换"""
        try:
            if target_type == 'int':
                return int(value)
            elif target_type == 'float':
                return float(value)
            elif target_type == 'bool':
                if isinstance(value, str):
                    return value.lower() in ('true', '1', 'yes', 'on')
                return bool(value)
            elif target_type == 'datetime':
                if isinstance(value, str):
                    return datetime.fromisoformat(value.replace('Z', '+00:00'))
                return value
            else:
                return str(value)
        except Exception as e:
            logger.warning(f"数据类型转换失败：{value} -> {target_type}, 错误：{e}")
            return None

class CSVAdapter(DataAdapter):
    """CSV数据适配器"""
    
    def read_data(self, source_path: str, **kwargs) -> List[Dict]:
        """读取CSV数据"""
        try:
            encoding = kwargs.get('encoding', 'utf-8')
            delimiter = kwargs.get('delimiter', ',')
            
            df = pd.read_csv(source_path, encoding=encoding, delimiter=delimiter)
            
            # 处理NaN值
            df = df.where(pd.notnull(df), None)
            
            data = df.to_dict('records')
            
            logger.info(f"成功读取CSV数据，共 {len(data)} 条记录")
            return data
        except Exception as e:
            logger.error(f"读取CSV数据失败：{e}")
            return []
    
    def validate_data(self, data: List[Dict]) -> bool:
        """验证CSV数据格式"""
        if not isinstance(data, list) or len(data) == 0:
            return False
        
        # 检查所有记录是否有相同的字段
        first_record_keys = set(data[0].keys())
        for record in data[1:]:
            if set(record.keys()) != first_record_keys:
                return False
        
        return True
    
    def transform_data(self, data: List[Dict], target_schema: Dict) -> List[Dict]:
        """转换CSV数据格式"""
        json_adapter = JSONAdapter()
        return json_adapter.transform_data(data, target_schema)

class XMLAdapter(DataAdapter):
    """XML数据适配器"""
    
    def read_data(self, source_path: str, **kwargs) -> List[Dict]:
        """读取XML数据"""
        try:
            tree = ET.parse(source_path)
            root = tree.getroot()
            
            # 获取记录节点名称
            record_tag = kwargs.get('record_tag', 'record')
            
            data = []
            for record_elem in root.findall(f'.//{record_tag}'):
                record = self._xml_element_to_dict(record_elem)
                data.append(record)
            
            logger.info(f"成功读取XML数据，共 {len(data)} 条记录")
            return data
        except Exception as e:
            logger.error(f"读取XML数据失败：{e}")
            return []
    
    def _xml_element_to_dict(self, element: ET.Element) -> Dict:
        """将XML元素转换为字典"""
        result = {}
        
        # 添加属性
        if element.attrib:
            result.update(element.attrib)
        
        # 添加子元素
        for child in element:
            if len(child) == 0:
                # 叶子节点
                result[child.tag] = child.text
            else:
                # 有子节点的元素
                if child.tag in result:
                    if not isinstance(result[child.tag], list):
                        result[child.tag] = [result[child.tag]]
                    result[child.tag].append(self._xml_element_to_dict(child))
                else:
                    result[child.tag] = self._xml_element_to_dict(child)
        
        # 如果只有文本内容
        if not result and element.text:
            return element.text
        
        return result
    
    def validate_data(self, data: List[Dict]) -> bool:
        """验证XML数据格式"""
        return isinstance(data, list) and all(isinstance(record, dict) for record in data)
    
    def transform_data(self, data: List[Dict], target_schema: Dict) -> List[Dict]:
        """转换XML数据格式"""
        json_adapter = JSONAdapter()
        return json_adapter.transform_data(data, target_schema)

class APIAdapter(DataAdapter):
    """API数据适配器"""
    
    def read_data(self, source_path: str, **kwargs) -> List[Dict]:
        """从API读取数据"""
        try:
            method = kwargs.get('method', 'GET')
            headers = kwargs.get('headers', {})
            params = kwargs.get('params', {})
            data = kwargs.get('data', {})
            timeout = kwargs.get('timeout', 30)
            
            if method.upper() == 'GET':
                response = requests.get(source_path, headers=headers, params=params, timeout=timeout)
            elif method.upper() == 'POST':
                response = requests.post(source_path, headers=headers, json=data, timeout=timeout)
            else:
                raise ValueError(f"不支持的HTTP方法：{method}")
            
            response.raise_for_status()
            
            api_data = response.json()
            
            # 处理API响应格式
            if isinstance(api_data, dict):
                # 尝试提取数据数组
                data_key = kwargs.get('data_key', 'data')
                if data_key in api_data:
                    api_data = api_data[data_key]
                else:
                    api_data = [api_data]
            elif isinstance(api_data, list):
                pass  # 已经是数组格式
            else:
                raise ValueError("API返回数据格式不正确")
            
            logger.info(f"成功从API读取数据，共 {len(api_data)} 条记录")
            return api_data
        except Exception as e:
            logger.error(f"从API读取数据失败：{e}")
            return []
    
    def validate_data(self, data: List[Dict]) -> bool:
        """验证API数据格式"""
        return isinstance(data, list) and all(isinstance(record, dict) for record in data)
    
    def transform_data(self, data: List[Dict], target_schema: Dict) -> List[Dict]:
        """转换API数据格式"""
        json_adapter = JSONAdapter()
        return json_adapter.transform_data(data, target_schema)

class DatabaseAdapter(DataAdapter):
    """数据库适配器"""
    
    def read_data(self, source_path: str, **kwargs) -> List[Dict]:
        """从数据库读取数据"""
        try:
            # source_path 格式：sqlite:///path/to/db.sqlite?table=table_name
            if source_path.startswith('sqlite:///'):
                db_path = source_path[10:].split('?')[0]
                table_name = kwargs.get('table', 'data')
                
                conn = sqlite3.connect(db_path)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                query = f"SELECT * FROM {table_name}"
                params = kwargs.get('params', [])
                
                if params:
                    where_clause = " AND ".join([f"{k} = ?" for k in params.keys()])
                    query += f" WHERE {where_clause}"
                    cursor.execute(query, list(params.values()))
                else:
                    cursor.execute(query)
                
                rows = cursor.fetchall()
                data = [dict(row) for row in rows]
                
                conn.close()
                
                logger.info(f"成功从数据库读取数据，共 {len(data)} 条记录")
                return data
            else:
                raise ValueError("仅支持SQLite数据库")
        except Exception as e:
            logger.error(f"从数据库读取数据失败：{e}")
            return []
    
    def validate_data(self, data: List[Dict]) -> bool:
        """验证数据库数据格式"""
        return isinstance(data, list) and all(isinstance(record, dict) for record in data)
    
    def transform_data(self, data: List[Dict], target_schema: Dict) -> List[Dict]:
        """转换数据库数据格式"""
        json_adapter = JSONAdapter()
        return json_adapter.transform_data(data, target_schema)

class AdapterFactory:
    """适配器工厂类"""
    
    _adapters = {
        'json': JSONAdapter,
        'csv': CSVAdapter,
        'xml': XMLAdapter,
        'api': APIAdapter,
        'database': DatabaseAdapter,
    }
    
    @classmethod
    def create_adapter(cls, adapter_type: str) -> DataAdapter:
        """创建适配器实例"""
        if adapter_type not in cls._adapters:
            raise ValueError(f"不支持的适配器类型：{adapter_type}")
        
        return cls._adapters[adapter_type]()
    
    @classmethod
    def register_adapter(cls, adapter_type: str, adapter_class: type):
        """注册新的适配器类型"""
        cls._adapters[adapter_type] = adapter_class
    
    @classmethod
    def get_supported_types(cls) -> List[str]:
        """获取支持的适配器类型"""
        return list(cls._adapters.keys())

class DataSchemaManager:
    """数据模式管理器"""
    
    def __init__(self, schema_file: str = "data_schemas.json"):
        self.schema_file = schema_file
        self.schemas = self._load_schemas()
    
    def _load_schemas(self) -> Dict:
        """加载数据模式"""
        default_schemas = {
            "medical_records": {
                "id": {"source_field": "id", "type": "int", "required": False},
                "patient_id": {"source_field": "patient_id", "type": "int", "required": True},
                "hospital_id": {"source_field": "hospital_id", "type": "int", "required": True},
                "department_id": {"source_field": "department_id", "type": "int", "required": True},
                "visit_type": {"source_field": "visit_type", "type": "int", "required": True},
                "visit_date": {"source_field": "visit_date", "type": "datetime", "required": True},
                "chief_complaint": {"source_field": "chief_complaint", "type": "string", "required": False},
                "diagnosis": {"source_field": "diagnosis", "type": "string", "required": False},
                "disease_code": {"source_field": "disease_code", "type": "string", "required": False},
                "disease_category": {"source_field": "disease_category", "type": "string", "required": False},
                "treatment_plan": {"source_field": "treatment_plan", "type": "string", "required": False},
                "created_at": {"source_field": "created_at", "type": "datetime", "required": False, "default": "now"}
            },
            "vital_signs": {
                "id": {"source_field": "id", "type": "int", "required": False},
                "record_id": {"source_field": "record_id", "type": "int", "required": True},
                "temperature": {"source_field": "temperature", "type": "float", "required": False},
                "blood_pressure_systolic": {"source_field": "blood_pressure_systolic", "type": "int", "required": False},
                "blood_pressure_diastolic": {"source_field": "blood_pressure_diastolic", "type": "int", "required": False},
                "heart_rate": {"source_field": "heart_rate", "type": "int", "required": False},
                "respiratory_rate": {"source_field": "respiratory_rate", "type": "int", "required": False},
                "oxygen_saturation": {"source_field": "oxygen_saturation", "type": "float", "required": False},
                "measure_time": {"source_field": "measure_time", "type": "datetime", "required": True},
                "created_at": {"source_field": "created_at", "type": "datetime", "required": False, "default": "now"}
            },
            "maternal_info": {
                "id": {"source_field": "id", "type": "int", "required": False},
                "patient_id": {"source_field": "patient_id", "type": "int", "required": True},
                "pregnancy_count": {"source_field": "pregnancy_count", "type": "int", "required": False},
                "gestational_weeks": {"source_field": "gestational_weeks", "type": "int", "required": False},
                "pregnancy_type": {"source_field": "pregnancy_type", "type": "string", "required": False},
                "risk_level": {"source_field": "risk_level", "type": "string", "required": False},
                "due_date": {"source_field": "due_date", "type": "datetime", "required": False},
                "notes": {"source_field": "notes", "type": "string", "required": False},
                "created_at": {"source_field": "created_at", "type": "datetime", "required": False, "default": "now"}
            }
        }
        
        if os.path.exists(self.schema_file):
            try:
                with open(self.schema_file, 'r', encoding='utf-8') as f:
                    loaded_schemas = json.load(f)
                    return {**default_schemas, **loaded_schemas}
            except Exception as e:
                logger.error(f"加载数据模式失败：{e}")
        
        # 保存默认模式
        self._save_schemas(default_schemas)
        return default_schemas
    
    def _save_schemas(self, schemas: Dict):
        """保存数据模式"""
        try:
            with open(self.schema_file, 'w', encoding='utf-8') as f:
                json.dump(schemas, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存数据模式失败：{e}")
    
    def get_schema(self, schema_name: str) -> Optional[Dict]:
        """获取指定的数据模式"""
        return self.schemas.get(schema_name)
    
    def add_schema(self, schema_name: str, schema: Dict):
        """添加新的数据模式"""
        self.schemas[schema_name] = schema
        self._save_schemas(self.schemas)
    
    def list_schemas(self) -> List[str]:
        """列出所有可用的数据模式"""
        return list(self.schemas.keys())

# 使用示例
if __name__ == "__main__":
    # 创建适配器
    json_adapter = AdapterFactory.create_adapter('json')
    
    # 创建模式管理器
    schema_manager = DataSchemaManager()
    
    # 读取和转换数据示例
    try:
        # 读取JSON数据
        data = json_adapter.read_data("example_data.json")
        
        # 获取数据模式
        schema = schema_manager.get_schema("medical_records")
        
        if schema:
            # 转换数据
            transformed_data = json_adapter.transform_data(data, schema)
            print(f"转换后的数据：{len(transformed_data)} 条记录")
        else:
            print("未找到数据模式")
    
    except Exception as e:
        print(f"示例执行失败：{e}")