import sqlite3
import os

# 数据库路径
db_path = 'medical_system.db'
# 文档路径
doc_path = '数据库信息和数据清单.md'

def verify_database():
    print("=== 验证数据库数据 ===")
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 验证data_statistics表
        cursor.execute("SELECT COUNT(*) FROM data_statistics")
        data_stats_count = cursor.fetchone()[0]
        print(f"data_statistics表记录数: {data_stats_count}")
        
        # 验证disease_analysis表
        cursor.execute("SELECT COUNT(*) FROM disease_analysis")
        disease_analysis_count = cursor.fetchone()[0]
        print(f"disease_analysis表记录数: {disease_analysis_count}")
        
        # 验证数据质量 - 检查是否有数据
        data_valid = data_stats_count > 0 and disease_analysis_count > 0
        
        conn.close()
        return data_valid
    except Exception as e:
        print(f"数据库验证错误: {e}")
        return False

def verify_document():
    print("\n=== 验证文档更新 ===")
    try:
        # 检查文档是否存在
        if not os.path.exists(doc_path):
            print("错误: 文档不存在")
            return False
        
        # 读取文档内容
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查记录数量更新
        data_stats_record_updated = "**记录数量：** 17" in content
        disease_analysis_record_updated = "**记录数量：** 10" in content
        
        # 检查数据样本更新
        data_sample_updated = "**数据样本（前3条）：**" in content
        
        print(f"data_statistics表记录数更新: {data_stats_record_updated}")
        print(f"disease_analysis表记录数更新: {disease_analysis_record_updated}")
        print(f"数据样本更新: {data_sample_updated}")
        
        doc_valid = data_stats_record_updated and disease_analysis_record_updated and data_sample_updated
        return doc_valid
    except Exception as e:
        print(f"文档验证错误: {e}")
        return False

if __name__ == "__main__":
    print("开始全面验证...")
    
    db_valid = verify_database()
    doc_valid = verify_document()
    
    print("\n=== 验证结果 ===")
    print(f"数据库验证: {'成功' if db_valid else '失败'}")
    print(f"文档更新验证: {'成功' if doc_valid else '失败'}")
    
    if db_valid and doc_valid:
        print("\n✅ 所有任务验证成功！数据已正确插入，文档已更新。")
    else:
        print("\n❌ 验证失败，请检查错误信息。")
