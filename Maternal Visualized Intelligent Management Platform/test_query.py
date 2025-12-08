# 测试querys函数是否能正确从数据库获取数据
from utils.query import querys

# 测试1: 查询所有表（使用SQLite兼容的方式）
try:
    print("测试1: 查询所有表（使用SQLite兼容的方式）")
    tables = querys("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    if tables:
        print(f"数据库中的表: {[table[0] for table in tables]}")
    else:
        print("数据库中的表: 无")
except Exception as e:
    print(f"测试1失败: {e}")

# 测试2: 查询medical_data表中的数据
try:
    print("\n测试2: 查询medical_data表中的数据")
    medical_data = querys("SELECT * FROM medical_data LIMIT 5")
    print(f"medical_data表前5条数据: {medical_data}")
except Exception as e:
    print(f"测试2失败: {e}")

# 测试3: 查询maternal_info表中的数据
try:
    print("\n测试3: 查询maternal_info表中的数据")
    maternal_data = querys("SELECT * FROM maternal_info LIMIT 5")
    print(f"maternal_info表前5条数据: {maternal_data}")
except Exception as e:
    print(f"测试3失败: {e}")

# 测试4: 使用getPublicData获取数据
try:
    print("\n测试4: 使用getPublicData获取数据")
    from utils.getPublicData import getAllCasesData
    data = getAllCasesData()
    print(f"getAllCasesData返回的数据类型: {type(data)}")
    if data:
        print(f"数据条数: {len(data)}")
        print(f"第一条数据: {data[0]}")
except Exception as e:
    print(f"测试4失败: {e}")
