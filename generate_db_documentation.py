# 生成数据库信息和数据清单的Markdown文件
import sqlite3
import os

# 连接到数据库
conn = sqlite3.connect('medical_system.db')
cursor = conn.cursor()

# 获取所有表名
def get_all_tables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    return [table[0] for table in cursor.fetchall()]

# 获取表的结构信息
def get_table_structure(table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return cursor.fetchall()

# 获取表的记录数量
def get_table_row_count(table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0]

# 获取表的创建语句
def get_table_create_statement(table_name):
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cursor.fetchone()
    return result[0] if result else ""

# 生成Markdown文档

def generate_markdown_documentation():
    tables = get_all_tables()
    
    # 文档头部
    markdown_content = "# 数据库信息和数据清单\n\n"
    markdown_content += "## 1. 数据库基本信息\n\n"
    markdown_content += "| 属性 | 数值 |\n"
    markdown_content += "|------|------|\n"
    markdown_content += "| 数据库名称 | medical_system.db |\n"
    markdown_content += "| 数据库类型 | SQLite |\n"
    markdown_content += "| 文件路径 | " + os.path.abspath('medical_system.db') + " |\n"
    markdown_content += "| 总表数量 | " + str(len(tables)) + " |\n\n"
    
    # 表结构和数据信息
    markdown_content += "## 2. 表结构和数据信息\n\n"
    
    for table in tables:
        structure = get_table_structure(table)
        row_count = get_table_row_count(table)
        create_stmt = get_table_create_statement(table)
        
        markdown_content += f"### 2.1 表名：{table}\n\n"
        markdown_content += f"**记录数量：** {row_count}\n\n"
        markdown_content += "**表结构：**\n\n"
        markdown_content += "| 字段名 | 数据类型 | 是否为主键 | 是否允许为空 | 描述 |\n"
        markdown_content += "|--------|----------|------------|--------------|------|\n"
        
        for column in structure:
            column_id, name, type_, notnull, dflt_value, pk = column
            pk_status = "是" if pk == 1 else "否"
            null_status = "否" if notnull == 1 else "是"
            
            markdown_content += f"| {name} | {type_} | {pk_status} | {null_status} | - |\n"
        
        markdown_content += "\n**创建语句：**\n\n"
        markdown_content += f"```sql\n{create_stmt}\n```\n\n"
        
        # 添加数据样本（只显示前3条）
        if row_count > 0:
            markdown_content += f"**数据样本（前3条）：**\n\n"
            
            cursor.execute(f"SELECT * FROM {table} LIMIT 3")
            sample_data = cursor.fetchall()
            
            if sample_data:
                # 获取列名
                column_names = [description[0] for description in cursor.description]
                
                # 创建表头
                markdown_content += "| " + " | ".join(column_names) + " |\n"
                markdown_content += "| " + " | ".join(["---"] * len(column_names)) + " |\n"
                
                # 添加数据行
                for row in sample_data:
                    # 将None值转换为"-"
                    row_values = [str(value) if value is not None else "-" for value in row]
                    markdown_content += "| " + " | ".join(row_values) + " |\n"
            
            markdown_content += "\n---\n\n"
    
    # 数据来源说明
    markdown_content += "## 3. 数据来源说明\n\n"
    markdown_content += "| 数据类型 | 来源 | 说明 |\n"
    markdown_content += "|----------|------|------|\n"
    markdown_content += "| 系统表 | 自动创建 | 用户角色、权限、系统配置等基础数据 |\n"
    markdown_content += "| 医疗数据 | 自动生成 | 从generate_test_data.py生成的模拟医疗数据 |\n"
    markdown_content += "| 孕产妇数据 | 自动生成 | 系统内置的模拟孕产妇数据生成功能 |\n"
    markdown_content += "| 统计数据 | 实时计算 | 基于医疗数据和孕产妇数据实时统计分析 |\n\n"
    
    # 数据质量说明
    markdown_content += "## 4. 数据质量说明\n\n"
    markdown_content += "- 所有数据均为模拟数据，用于系统测试和演示\n"
    markdown_content += "- 医疗数据包含真实的疾病类型、症状和治疗方法\n"
    markdown_content += "- 数据符合医疗行业的基本规范和逻辑\n"
    markdown_content += "- 数据量适中，适合系统性能测试\n\n"
    
    # 最后更新时间
    import datetime
    markdown_content += "**最后更新时间：** " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    
    return markdown_content

# 生成文档并保存到文件

if __name__ == "__main__":
    try:
        markdown_doc = generate_markdown_documentation()
        
        # 保存到文件
        with open("数据库信息和数据清单.md", "w", encoding="utf-8") as file:
            file.write(markdown_doc)
        
        print("\n✅ 数据库文档已成功生成！")
        print("📄 文件路径：" + os.path.abspath("数据库信息和数据清单.md"))
        
        # 统计信息
        tables = get_all_tables()
        print(f"\n📊 文档统计：")
        print(f"   - 记录的表数量：{len(tables)}")
        
        total_records = sum(get_table_row_count(table) for table in tables)
        print(f"   - 数据库总记录数：{total_records}")
        
    except Exception as e:
        print(f"❌ 生成文档时出错：{e}")
    finally:
        # 关闭数据库连接
        conn.close()
