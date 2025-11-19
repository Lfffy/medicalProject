def display_uml_content():
    # 读取UML文件内容
    uml_file_path = r"d:\文档\作业\软工\基于python医疗疾病数据分析大屏可视化系统\Untitled-1"
    
    try:
        with open(uml_file_path, 'r', encoding='utf-8') as f:
            uml_content = f.read()
        
        print("===== UML 文件内容 =====")
        print(uml_content)
        print("=======================")
        
        # 提供使用方法
        print("\n为了运行这个UML文件，您可以：")
        print("1. 访问 https://www.plantuml.com/plantuml/uml/")
        print("2. 复制上面的UML内容到输入框")
        print("3. 点击Generate按钮生成图表")
        
    except Exception as e:
        print(f"读取UML文件时出错: {e}")

if __name__ == "__main__":
    display_uml_content()