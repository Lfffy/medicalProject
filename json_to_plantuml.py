import json
import re

def convert_json_to_plantuml():
    # 读取JSON格式的UML文件
    uml_file_path = r"d:\文档\作业\软工\基于python医疗疾病数据分析大屏可视化系统\Untitled-1"
    
    try:
        with open(uml_file_path, 'r', encoding='utf-8') as f:
            # 清理文件内容中的控制字符和格式问题
            content = f.read()
            # 移除可能的控制字符和多余的空格
            content = re.sub(r'[\x00-\x1f\x7f]', '', content)
            # 尝试解析JSON
            data = json.loads(content)
        
        # 开始构建PlantUML内容
        plantuml_content = "@startuml\n\nskinparam backgroundColor white\nskinparam handwritten false\n\n"
        
        # 提取并转换图中元素
        for diagram in data.get('diagrams', []):
            # 处理Actor
            actors = {}
            for element in diagram.get('elements', []):
                if element.get('type') == 'Actor':
                    actor_id = element.get('id')
                    actor_name = element.get('name', '').strip()
                    actors[actor_id] = actor_name
                    plantuml_content += f"actor \"{actor_name}\" as {actor_id}\n"
            
            plantuml_content += "\n"
            
            # 处理UseCase
            use_cases = {}
            for element in diagram.get('elements', []):
                if element.get('type') == 'UseCase':
                    uc_id = element.get('id')
                    uc_name = element.get('name', '').strip()
                    use_cases[uc_id] = uc_name
                    plantuml_content += f"usecase \"{uc_name}\" as {uc_id}\n"
            
            plantuml_content += "\n"
            
            # 处理Generalization (泛化关系)
            for element in diagram.get('elements', []):
                if element.get('type') == 'Generalization':
                    source = element.get('source')
                    target = element.get('target')
                    plantuml_content += f"{source} --|> {target}\n"
            
            plantuml_content += "\n"
            
            # 处理Association (关联关系)
            for element in diagram.get('elements', []):
                if element.get('type') == 'Association':
                    source = element.get('source')
                    target = element.get('target')
                    plantuml_content += f"{source} --> {target}\n"
        
        plantuml_content += "\n@enduml"
        
        # 保存PlantUML格式的内容到新文件
        plantuml_file_path = r"d:\文档\作业\软工\基于python医疗疾病数据分析大屏可视化系统\converted_uml.puml"
        with open(plantuml_file_path, 'w', encoding='utf-8') as f:
            f.write(plantuml_content)
        
        print(f"成功将JSON格式的UML转换为PlantUML格式")
        print(f"转换后的文件已保存到: {plantuml_file_path}")
        print("\nPlantUML内容:")
        print(plantuml_content)
        print("\n您可以使用以下方法渲染这个UML图:")
        print("1. 访问 https://www.plantuml.com/plantuml/uml/")
        print("2. 复制上面的PlantUML内容到输入框")
        print("3. 点击Generate按钮生成图表")
        
    except json.JSONDecodeError as e:
        print(f"解析JSON时出错: {e}")
        print("文件内容可能不是有效的JSON格式")
    except Exception as e:
        print(f"转换过程中出错: {e}")

if __name__ == "__main__":
    convert_json_to_plantuml()