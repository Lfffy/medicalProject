import sqlite3

# 连接到数据库
conn = sqlite3.connect('medical_system.db')
cursor = conn.cursor()

# 检查patients表结构
print("\nChecking patients table structure:")
cursor.execute("PRAGMA table_info(patients)")
patients_structure = cursor.fetchall()
for col in patients_structure:
    print(f"  {col[1]} ({col[2]})")

# 检查vital_signs表结构
print("\nChecking vital_signs table structure:")
cursor.execute("PRAGMA table_info(vital_signs)")
vital_signs_structure = cursor.fetchall()
for col in vital_signs_structure:
    print(f"  {col[1]} ({col[2]})")

# 检查是否有数据
print("\nChecking if tables have data:")
cursor.execute("SELECT COUNT(*) FROM patients")
patients_count = cursor.fetchone()[0]
print(f"  Patients table has {patients_count} records")

cursor.execute("SELECT COUNT(*) FROM vital_signs")
vital_signs_count = cursor.fetchone()[0]
print(f"  Vital_signs table has {vital_signs_count} records")

# 测试查询
print("\nTesting the vital signs query:")
try:
    query = """
    SELECT 
        p.id,
        p.name,
        p.age,
        vs.systolic_pressure,
        vs.diastolic_pressure,
        vs.heart_rate,
        vs.body_temperature,
        vs.blood_oxygen,
        vs.created_at
    FROM patients p
    LEFT JOIN vital_signs vs ON p.id = vs.record_id
    ORDER BY vs.created_at DESC
    LIMIT 5
    """
    cursor.execute(query)
    results = cursor.fetchall()
    print(f"  Query returned {len(results)} rows")
    if results:
        print("  Sample data:")
        for row in results:
            print(f"    ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")
except Exception as e:
    print(f"  Query failed: {str(e)}")

conn.close()
