class PredictionExplainer:
    """模型预测解释器的简化实现"""
    
    def __init__(self):
        print("初始化简化版预测解释器")
    
    def explain_prediction(self, model_type, prediction_proba, features):
        """解释预测结果"""
        # 模拟解释结果
        explanations = {
            'preeclampsia': {
                'top_features': ['年龄', '收缩压', '舒张压'],
                'contributions': [0.3, 0.25, 0.2],
                'interpretation': '基于您的血压和年龄进行风险评估'
            },
            'gestational_diabetes': {
                'top_features': ['BMI', '年龄', '家族史'],
                'contributions': [0.25, 0.2, 0.15],
                'interpretation': '综合考虑您的身体指标和家族史'
            },
            'preterm_birth': {
                'top_features': ['宫颈长度', '年龄', '既往史'],
                'contributions': [0.35, 0.15, 0.1],
                'interpretation': '主要基于宫颈情况评估早产风险'
            }
        }
        
        return explanations.get(model_type, {
            'top_features': [],
            'contributions': [],
            'interpretation': '使用默认解释'
        })
    
    def get_feature_importance(self, model_type):
        """获取特征重要性"""
        # 返回模拟的特征重要性
        importance = {
            'preeclampsia': {
                '收缩压': 0.35,
                '舒张压': 0.3,
                '年龄': 0.2,
                'BMI': 0.15
            },
            'gestational_diabetes': {
                '空腹血糖': 0.4,
                'BMI': 0.3,
                '年龄': 0.2,
                '家族史': 0.1
            },
            'preterm_birth': {
                '宫颈长度': 0.45,
                '年龄': 0.2,
                '既往史': 0.2,
                '炎症指标': 0.15
            }
        }
        
        return importance.get(model_type, {})

# 创建全局实例供导入使用
explainer = PredictionExplainer()