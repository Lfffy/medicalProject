import sqlite3
import json
import datetime

# 数据库路径
db_path = 'medical_system.db'

def insert_disease_data():
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 清空现有数据
        cursor.execute("DELETE FROM disease_analysis")
        print("已清空disease_analysis表中的现有数据")
        
        # 获取当前时间用于created_at和updated_at
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # 准备示例数据（基于妇产科常见疾病，使用正确的列名）
        disease_data = [
            # 高风险疾病
            {
                'disease_name': '妊娠期高血压',
                'disease_category': '妊娠期并发症',
                'incidence_rate': 8.5,
                'mortality_rate': 0.2,
                'age_group': '20-49岁',
                'gender_distribution': json.dumps({'女性': 100.0}),
                'risk_factors': json.dumps({'年龄>35岁': 3.2, '肥胖': 2.5, '有家族史': 2.8, '慢性高血压': 5.0}),
                'symptoms': '高血压、蛋白尿、水肿、头痛、视觉障碍等',
                'treatment_methods': '休息、药物治疗（如硫酸镁）、密切监测、适时终止妊娠',
                'prevention_methods': '定期产检、控制体重、低盐饮食、适度运动、监测血压',
                'analysis_date': current_date,
                'data_source': '医院统计数据'
            },
            {
                'disease_name': '妊娠期糖尿病',
                'disease_category': '妊娠期并发症',
                'incidence_rate': 12.3,
                'mortality_rate': 0.1,
                'age_group': '20-49岁',
                'gender_distribution': json.dumps({'女性': 100.0}),
                'risk_factors': json.dumps({'年龄>35岁': 2.8, '肥胖': 3.5, '有家族史': 3.2, '既往GDM史': 4.5}),
                'symptoms': '多饮、多尿、多食、体重增加异常、羊水过多等',
                'treatment_methods': '饮食控制、运动疗法、胰岛素治疗、血糖监测',
                'prevention_methods': '健康饮食、适量运动、控制体重、定期血糖监测、高危人群早期筛查',
                'analysis_date': current_date,
                'data_source': '医院统计数据'
            },
            {
                'disease_name': '前置胎盘',
                'disease_category': '胎盘异常',
                'incidence_rate': 2.5,
                'mortality_rate': 0.5,
                'age_group': '20-49岁',
                'gender_distribution': json.dumps({'女性': 100.0}),
                'risk_factors': json.dumps({'多次刮宫史': 4.2, '多胎妊娠': 2.5, '高龄产妇': 2.8, '吸烟': 1.8}),
                'symptoms': '无痛性阴道出血、贫血、休克等',
                'treatment_methods': '期待疗法、药物治疗、必要时输血、剖宫产终止妊娠',
                'prevention_methods': '避免多次刮宫、注意孕期保健、避免吸烟',
                'analysis_date': current_date,
                'data_source': '医院统计数据'
            },
            # 中风险疾病
            {
                'disease_name': '妊娠期贫血',
                'disease_category': '妊娠期并发症',
                'incidence_rate': 25.8,
                'mortality_rate': 0.05,
                'age_group': '20-49岁',
                'gender_distribution': json.dumps({'女性': 100.0}),
                'risk_factors': json.dumps({'铁摄入不足': 3.5, '孕吐严重': 2.8, '多胎妊娠': 3.2, '月经过多': 2.5}),
                'symptoms': '乏力、头晕、心悸、气短、面色苍白等',
                'treatment_methods': '口服铁剂、饮食调整、输血（严重贫血时）',
                'prevention_methods': '补充铁剂、叶酸、维生素B12、均衡饮食',
                'analysis_date': current_date,
                'data_source': '医院统计数据'
            },
            {
                'disease_name': '羊水过多',
                'disease_category': '羊水异常',
                'incidence_rate': 3.5,
                'mortality_rate': 0.3,
                'age_group': '20-49岁',
                'gender_distribution': json.dumps({'女性': 100.0}),
                'risk_factors': json.dumps({'妊娠期糖尿病': 4.5, '胎儿畸形': 3.8, '多胎妊娠': 3.2, 'Rh血型不合': 2.5}),
                'symptoms': '腹部增大过快、呼吸困难、下肢水肿等',
                'treatment_methods': '病因治疗、羊膜腔穿刺放液、适时终止妊娠',
                'prevention_methods': '积极治疗糖尿病等原发病、定期产检',
                'analysis_date': current_date,
                'data_source': '医院统计数据'
            },
            # 低风险疾病
            {
                'disease_name': '妊娠期牙龈炎',
                'disease_category': '妊娠期口腔疾病',
                'incidence_rate': 45.2,
                'mortality_rate': 0.0,
                'age_group': '20-49岁',
                'gender_distribution': json.dumps({'女性': 100.0}),
                'risk_factors': json.dumps({'激素变化': 3.2, '口腔卫生不良': 4.5, '既往牙龈病史': 2.8, '维生素C缺乏': 2.0}),
                'symptoms': '牙龈红肿、出血、疼痛等',
                'treatment_methods': '口腔清洁、局部用药、定期洗牙',
                'prevention_methods': '保持口腔卫生、定期口腔检查、正确刷牙',
                'analysis_date': current_date,
                'data_source': '医院统计数据'
            },
            {
                'disease_name': '妊娠期便秘',
                'disease_category': '妊娠期消化系统疾病',
                'incidence_rate': 60.5,
                'mortality_rate': 0.0,
                'age_group': '20-49岁',
                'gender_distribution': json.dumps({'女性': 100.0}),
                'risk_factors': json.dumps({'激素变化': 3.5, '活动减少': 2.8, '膳食纤维不足': 3.2, '铁剂治疗': 2.5}),
                'symptoms': '排便困难、大便干燥、排便次数减少等',
                'treatment_methods': '饮食调整、适当运动、使用缓泻剂',
                'prevention_methods': '多吃膳食纤维、多喝水、适量运动、养成良好排便习惯',
                'analysis_date': current_date,
                'data_source': '医院统计数据'
            },
            # 妇科疾病
            {
                'disease_name': '功能性子宫出血',
                'disease_category': '妇科内分泌疾病',
                'incidence_rate': 15.2,
                'mortality_rate': 0.1,
                'age_group': '15-55岁',
                'gender_distribution': json.dumps({'女性': 100.0}),
                'risk_factors': json.dumps({'压力过大': 2.5, '过度运动': 1.8, '肥胖': 2.2, '甲状腺功能异常': 3.0}),
                'symptoms': '月经周期紊乱、经量过多、经期延长等',
                'treatment_methods': '激素治疗、刮宫术、止血药物、手术治疗',
                'prevention_methods': '保持健康生活方式、定期妇科检查、避免过度劳累',
                'analysis_date': current_date,
                'data_source': '医院统计数据'
            },
            {
                'disease_name': '子宫内膜异位症',
                'disease_category': '妇科良性疾病',
                'incidence_rate': 10.8,
                'mortality_rate': 0.0,
                'age_group': '20-45岁',
                'gender_distribution': json.dumps({'女性': 100.0}),
                'risk_factors': json.dumps({'家族史': 3.5, '经期倒流': 2.8, '晚育': 2.2, '免疫功能异常': 1.8}),
                'symptoms': '痛经、慢性盆腔痛、性交痛、不孕等',
                'treatment_methods': '药物治疗、手术治疗、辅助生殖技术',
                'prevention_methods': '及时治疗宫颈粘连、避免经期性生活、减少医源性种植',
                'analysis_date': current_date,
                'data_source': '医院统计数据'
            },
            {
                'disease_name': '宫颈糜烂',
                'disease_category': '宫颈病变',
                'incidence_rate': 30.5,
                'mortality_rate': 0.0,
                'age_group': '20-50岁',
                'gender_distribution': json.dumps({'女性': 100.0}),
                'risk_factors': json.dumps({'性生活过早': 3.2, '多个性伴侣': 2.8, '吸烟': 1.5, 'HPV感染': 4.5}),
                'symptoms': '白带增多、接触性出血、外阴瘙痒等',
                'treatment_methods': '观察、药物治疗、物理治疗、手术治疗',
                'prevention_methods': '注意性生活卫生、定期宫颈癌筛查、避免多个性伴侣',
                'analysis_date': current_date,
                'data_source': '医院统计数据'
            }
        ]
        
        # 插入数据
        inserted_count = 0
        for data in disease_data:
            cursor.execute(
                "INSERT INTO disease_analysis (disease_name, disease_category, incidence_rate, mortality_rate, "
                "age_group, gender_distribution, risk_factors, symptoms, treatment_methods, "
                "prevention_methods, analysis_date, data_source, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (data['disease_name'], data['disease_category'], data['incidence_rate'], data['mortality_rate'],
                 data['age_group'], data['gender_distribution'], data['risk_factors'], data['symptoms'],
                 data['treatment_methods'], data['prevention_methods'], data['analysis_date'], data['data_source'],
                 now, now)
            )
            inserted_count += 1
        
        # 提交事务
        conn.commit()
        print(f"成功插入{inserted_count}条疾病分析数据")
        
        # 验证插入结果 - 显示前5条记录
        cursor.execute("SELECT id, disease_name, incidence_rate, disease_category, created_at FROM disease_analysis LIMIT 5")
        rows = cursor.fetchall()
        
        print("\n插入的数据预览（前5条）：")
        for row in rows:
            print(f"ID: {row[0]}, 疾病名称: {row[1]}, 发病率: {row[2]}%, 疾病类别: {row[3]}, 创建时间: {row[4]}")
        
    except Exception as e:
        print(f"插入数据时出错: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    insert_disease_data()
