import plantuml
import os

def run_plantuml():
    # 读取UML文件内容
    uml_file_path = r"d:\文档\作业\软工\基于python医疗疾病数据分析大屏可视化系统\Untitled-1"
    
    try:
        with open(uml_file_path, 'r', encoding='utf-8') as f:
            uml_content = f.read()
        
        # 初始化PlantUML实例
        plantuml_instance = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')
        
        # 生成图像
        output_file = r"d:\文档\作业\软工\基于python医疗疾病数据分析大屏可视化系统\uml_diagram.png"
        plantuml_instance.processes_file(uml_file_path, outfile=output_file)
        
        print(f"UML图表已成功生成: {output_file}")
        
    except Exception as e:
        print(f"处理UML文件时出错: {e}")
        
        # 如果在线服务失败，尝试保存处理后的UML内容到文件
        try:
            with open("processed_uml.txt", "w", encoding="utf-8") as f:
                f.write(uml_content)
            print("UML内容已保存到 processed_uml.txt")
        except:
            pass

if __name__ == "__main__":
    run_plantuml()