#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目清理脚本
删除无用的缓存文件、测试文件、重复文件等
"""

import os
import shutil
import glob
import json
from pathlib import Path

class ProjectCleaner:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.deleted_files = []
        self.deleted_dirs = []
        self.errors = []
    
    def log_action(self, action, path):
        """记录删除操作"""
        print(f"{action}: {path}")
        if action.startswith("删除文件"):
            self.deleted_files.append(str(path))
        elif action.startswith("删除目录"):
            self.deleted_dirs.append(str(path))
    
    def log_error(self, error):
        """记录错误"""
        print(f"错误: {error}")
        self.errors.append(error)
    
    def delete_pycache_files(self):
        """删除Python缓存文件"""
        print("\n=== 删除Python缓存文件 ===")
        
        # 查找所有__pycache__目录
        pycache_dirs = list(self.project_root.rglob("__pycache__"))
        
        for pycache_dir in pycache_dirs:
            try:
                if pycache_dir.exists():
                    shutil.rmtree(pycache_dir)
                    self.log_action("删除目录", pycache_dir)
            except Exception as e:
                self.log_error(f"无法删除 {pycache_dir}: {e}")
        
        # 删除.pyc文件
        pyc_files = list(self.project_root.rglob("*.pyc"))
        for pyc_file in pyc_files:
            try:
                if pyc_file.exists():
                    pyc_file.unlink()
                    self.log_action("删除文件", pyc_file)
            except Exception as e:
                self.log_error(f"无法删除 {pyc_file}: {e}")
    
    def delete_test_files(self):
        """删除测试文件"""
        print("\n=== 删除测试文件 ===")
        
        test_files = [
            "api_test.py",
            "api_test_report.json", 
            "browser_compatibility_test.py",
            "browser_compatibility_test.html",
            "compatibility_check.py",
            "compatibility_test.html",
            "compatibility_test_report.json",
            "corrected_api_test.py",
            "corrected_api_test_report.json",
            "check_tables.py",
            "real_api_test.py",
            "real_api_test_report.json",
            "simple_compatibility_test.py",
            "system_function_test.py",
            "system_function_test_report.json",
            "test_api_endpoints.py",
            "test_app.py",
            "test_data_generation.sql",
            "test_simple.py"
        ]
        
        for test_file in test_files:
            file_path = self.project_root / test_file
            if file_path.exists():
                try:
                    file_path.unlink()
                    self.log_action("删除文件", file_path)
                except Exception as e:
                    self.log_error(f"无法删除 {file_path}: {e}")
    
    def delete_duplicate_venvs(self):
        """删除重复的虚拟环境"""
        print("\n=== 删除重复的虚拟环境 ===")
        
        # 保留.venv，删除new_venv
        new_venv = self.project_root / "new_venv"
        if new_venv.exists():
            try:
                shutil.rmtree(new_venv)
                self.log_action("删除目录", new_venv)
            except Exception as e:
                self.log_error(f"无法删除 {new_venv}: {e}")
    
    def delete_installation_files(self):
        """删除安装包文件"""
        print("\n=== 删除安装包文件 ===")
        
        installation_files = [
            "node-v12.16.1-x64.msi",
            "python-3.8.0-amd64.exe"
        ]
        
        for install_file in installation_files:
            file_path = self.project_root / install_file
            if file_path.exists():
                try:
                    file_path.unlink()
                    self.log_action("删除文件", file_path)
                except Exception as e:
                    self.log_error(f"无法删除 {file_path}: {e}")
    
    def delete_duplicate_databases(self):
        """删除重复的数据库文件（需要确认）"""
        print("\n=== 检查重复数据库文件 ===")
        
        # 列出所有.db文件
        db_files = list(self.project_root.glob("*.db"))
        print("发现的数据库文件:")
        for db_file in db_files:
            print(f"  - {db_file.name}")
        
        # 暂时不自动删除数据库文件，让用户确认
        print("数据库文件需要手动确认后删除")
    
    def delete_log_files(self):
        """删除日志文件"""
        print("\n=== 删除日志文件 ===")
        
        log_files = [
            "database_setup.log"
        ]
        
        for log_file in log_files:
            file_path = self.project_root / log_file
            if file_path.exists():
                try:
                    file_path.unlink()
                    self.log_action("删除文件", file_path)
                except Exception as e:
                    self.log_error(f"无法删除 {file_path}: {e}")
    
    def delete_temp_files(self):
        """删除临时文件"""
        print("\n=== 删除临时文件 ===")
        
        temp_files = [
            "data_summary.json"
        ]
        
        for temp_file in temp_files:
            file_path = self.project_root / temp_file
            if file_path.exists():
                try:
                    file_path.unlink()
                    self.log_action("删除文件", file_path)
                except Exception as e:
                    self.log_error(f"无法删除 {file_path}: {e}")
    
    def delete_duplicate_sql_files(self):
        """删除重复的SQL文件"""
        print("\n=== 检查重复SQL文件 ===")
        
        sql_files = list(self.project_root.glob("*.sql"))
        print("发现的SQL文件:")
        for sql_file in sql_files:
            print(f"  - {sql_file.name}")
        
        # 可以删除明显重复的测试数据文件
        duplicate_sql = [
            "sqlite_test_data_simple.sql"
        ]
        
        for sql_file in duplicate_sql:
            file_path = self.project_root / sql_file
            if file_path.exists():
                try:
                    file_path.unlink()
                    self.log_action("删除文件", file_path)
                except Exception as e:
                    self.log_error(f"无法删除 {file_path}: {e}")
    
    def generate_report(self):
        """生成清理报告"""
        print("\n" + "="*50)
        print("清理报告")
        print("="*50)
        print(f"删除的文件数量: {len(self.deleted_files)}")
        print(f"删除的目录数量: {len(self.deleted_dirs)}")
        print(f"遇到的错误数量: {len(self.errors)}")
        
        if self.deleted_files:
            print("\n删除的文件:")
            for file_path in self.deleted_files:
                print(f"  - {file_path}")
        
        if self.deleted_dirs:
            print("\n删除的目录:")
            for dir_path in self.deleted_dirs:
                print(f"  - {dir_path}")
        
        if self.errors:
            print("\n错误:")
            for error in self.errors:
                print(f"  - {error}")
        
        # 保存报告到文件
        report = {
            "deleted_files": self.deleted_files,
            "deleted_dirs": self.deleted_dirs,
            "errors": self.errors,
            "summary": {
                "files_deleted": len(self.deleted_files),
                "dirs_deleted": len(self.deleted_dirs),
                "errors": len(self.errors)
            }
        }
        
        report_file = self.project_root / "cleanup_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细报告已保存到: {report_file}")
    
    def run_cleanup(self):
        """执行完整清理"""
        print("开始项目清理...")
        print(f"项目根目录: {self.project_root}")
        
        self.delete_pycache_files()
        self.delete_test_files()
        self.delete_duplicate_venvs()
        self.delete_installation_files()
        self.delete_log_files()
        self.delete_temp_files()
        self.delete_duplicate_sql_files()
        self.delete_duplicate_databases()
        
        self.generate_report()

def main():
    # 获取项目根目录
    current_dir = Path(__file__).parent
    project_root = current_dir / "基于python医疗疾病数据分析大屏可视化系统"
    
    if not project_root.exists():
        print(f"错误: 项目目录不存在: {project_root}")
        return
    
    # 确认操作
    print(f"将要清理的项目目录: {project_root}")
    response = input("确认开始清理? (y/N): ")
    
    if response.lower() in ['y', 'yes', '是']:
        cleaner = ProjectCleaner(project_root)
        cleaner.run_cleanup()
    else:
        print("清理操作已取消")

if __name__ == "__main__":
    main()