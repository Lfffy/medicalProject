"""
机器学习预测模块
包含多种先进的机器学习算法用于医疗数据预测
"""

import numpy as np
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LSTM
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import xgboost as xgb
import lightgbm as lgb
import torch
import torch.nn as nn
import torch.optim as optim
import joblib
import warnings
warnings.filterwarnings('ignore')

class MedicalMLPredictor:
    """医疗机器学习预测器"""
    
    def __init__(self, model_dir="ml_models"):
        self.model_dir = model_dir
        self.scalers = {}
        self.encoders = {}
        self.models = {}
        self.trained_models = {}
        
        # 创建模型保存目录
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
    
    def getData(self, file_path):
        """读取JSON数据文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return pd.DataFrame(data)
        except Exception as e:
            print(f"读取文件 {file_path} 失败: {e}")
            return pd.DataFrame()
    
    def load_and_prepare_data(self):
        """加载和准备医疗数据"""
        try:
            # 加载数据 - 修正路径
            base_path = os.path.dirname(__file__)  # 当前文件所在目录
            medical_records_path = os.path.join(base_path, 'data', 'medical_records.json')
            vital_signs_path = os.path.join(base_path, 'data', 'vital_signs.json')
            maternal_path = os.path.join(base_path, 'data', 'maternal_info.json')
            
            # 使用getData函数加载数据
            df_medical = self.getData(medical_records_path)
            df_vital = self.getData(vital_signs_path)
            df_maternal = self.getData(maternal_path)
            
            return df_medical, df_vital, df_maternal
            
        except Exception as e:
            print(f"数据加载错误: {e}")
            return None, None, None
    
    def prepare_medical_features(self, df_medical, df_vital):
        """准备医疗特征数据"""
        try:
            # 合并医疗记录和生命体征数据
            df_merged = df_medical.merge(df_vital, left_on='id', right_on='record_id', how='left')
            
            # 特征工程
            features = []
            labels = []
            
            for _, row in df_merged.iterrows():
                # 基础特征
                feature_vector = [
                    row.get('hospital_id', 0),
                    row.get('department_id', 0),
                    row.get('visit_type', 0),
                    row.get('temperature', 36.5),
                    row.get('blood_pressure_systolic', 120),
                    row.get('blood_pressure_diastolic', 80),
                    row.get('heart_rate', 70),
                    row.get('respiratory_rate', 16),
                    row.get('oxygen_saturation', 98)
                ]
                
                # 时间特征
                if 'visit_date' in row and pd.notna(row['visit_date']):
                    visit_date = pd.to_datetime(row['visit_date'])
                    feature_vector.extend([
                        visit_date.hour,
                        visit_date.dayofweek,
                        visit_date.month
                    ])
                else:
                    feature_vector.extend([12, 1, 1])  # 默认值
                
                # 计算衍生特征
                if pd.notna(row.get('blood_pressure_systolic')) and pd.notna(row.get('blood_pressure_diastolic')):
                    pulse_pressure = row['blood_pressure_systolic'] - row['blood_pressure_diastolic']
                    map_pressure = row['blood_pressure_diastolic'] + pulse_pressure / 3
                    feature_vector.extend([pulse_pressure, map_pressure])
                else:
                    feature_vector.extend([40, 93])  # 默认值
                
                # 体温分类特征
                temp = row.get('temperature', 36.5)
                if temp > 37.5:
                    temp_category = 2  # 发热
                elif temp < 36.0:
                    temp_category = 0  # 体温过低
                else:
                    temp_category = 1  # 正常
                feature_vector.append(temp_category)
                
                features.append(feature_vector)
                
                # 标签：疾病类别
                disease_category = row.get('disease_category', '其他')
                labels.append(disease_category)
            
            return np.array(features), np.array(labels)
            
        except Exception as e:
            print(f"特征准备错误: {e}")
            return None, None
    
    def create_neural_network(self, input_dim, num_classes):
        """创建神经网络模型"""
        model = Sequential([
            Dense(128, activation='relu', input_shape=(input_dim,)),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(64, activation='relu'),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(32, activation='relu'),
            BatchNormalization(),
            Dropout(0.2),
            
            Dense(16, activation='relu'),
            Dropout(0.2),
            
            Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_disease_classification_model(self):
        """训练疾病分类模型"""
        try:
            print("开始训练疾病分类模型...")
            
            # 加载数据
            df_medical, df_vital, df_maternal = self.load_and_prepare_data()
            if df_medical is None:
                return None
            
            # 准备特征和标签
            X, y = self.prepare_medical_features(df_medical, df_vital)
            if X is None:
                return None
            
            # 检查类别分布
            from collections import Counter
            class_counts = Counter(y)
            print(f"类别分布: {class_counts}")
            
            # 过滤掉样本数少于2的类别
            valid_classes = [cls for cls, count in class_counts.items() if count >= 2]
            if len(valid_classes) < 2:
                print("有效类别数少于2，无法训练分类模型")
                return None
            
            # 过滤数据
            valid_indices = [i for i, label in enumerate(y) if label in valid_classes]
            X_filtered = X[valid_indices]
            y_filtered = [y[i] for i in valid_indices]
            
            # 编码标签
            le = LabelEncoder()
            y_encoded = le.fit_transform(y_filtered)
            
            # 特征标准化
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_filtered)
            
            # 分割数据 - 使用普通分割而不是分层分割
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y_encoded, test_size=0.2, random_state=42
            )
            
            # 定义模型
            models = {
                'neural_network': self.create_neural_network(X_train.shape[1], len(le.classes_)),
                'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
                'xgboost': xgb.XGBClassifier(random_state=42),
                'lightgbm': lgb.LGBMClassifier(random_state=42),
                'svm': SVC(probability=True, random_state=42),
                'logistic_regression': LogisticRegression(random_state=42, max_iter=1000)
            }
            
            results = {}
            
            # 训练和评估每个模型
            for name, model in models.items():
                print(f"训练 {name} 模型...")
                
                if name == 'neural_network':
                    # 神经网络特殊处理
                    early_stopping = EarlyStopping(patience=10, restore_best_weights=True)
                    reduce_lr = ReduceLROnPlateau(patience=5, factor=0.5)
                    
                    history = model.fit(
                        X_train, y_train,
                        validation_data=(X_test, y_test),
                        epochs=100,
                        batch_size=32,
                        callbacks=[early_stopping, reduce_lr],
                        verbose=0
                    )
                    
                    # 评估
                    y_pred = model.predict(X_test)
                    y_pred_classes = np.argmax(y_pred, axis=1)
                    accuracy = accuracy_score(y_test, y_pred_classes)
                    
                    results[name] = {
                        'accuracy': accuracy,
                        'history': history.history,
                        'predictions': y_pred_classes.tolist()
                    }
                    
                else:
                    # 传统机器学习模型
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    accuracy = accuracy_score(y_test, y_pred)
                    
                    results[name] = {
                        'accuracy': accuracy,
                        'predictions': y_pred.tolist()
                    }
                
                print(f"{name} 准确率: {accuracy:.4f}")
            
            # 保存最佳模型
            best_model_name = max(results.keys(), key=lambda x: results[x]['accuracy'])
            best_model = models[best_model_name]  # 从原始模型字典中获取
            
            # 保存模型和预处理器
            self.save_model(best_model, 'disease_classifier', best_model_name)
            self.save_preprocessor(scaler, 'disease_scaler')
            self.save_preprocessor(le, 'disease_encoder')
            
            print(f"最佳模型: {best_model_name}, 准确率: {results[best_model_name]['accuracy']:.4f}")
            
            return {
                'best_model': best_model_name,
                'accuracy': results[best_model_name]['accuracy'],
                'all_results': results,
                'label_classes': le.classes_.tolist(),
                'feature_names': self.get_feature_names()
            }
            
        except Exception as e:
            print(f"模型训练错误: {e}")
            return None
    
    def train_vital_signs_prediction(self):
        """训练生命体征预测模型"""
        try:
            print("开始训练生命体征预测模型...")
            
            # 加载数据
            df_medical, df_vital, df_maternal = self.load_and_prepare_data()
            if df_vital is None:
                return None
            
            # 准备时间序列数据
            df_vital_sorted = df_vital.sort_values('measure_time')
            
            # 创建时间序列特征
            features = []
            targets = []
            
            # 使用滑动窗口创建时间序列
            window_size = 3
            
            for i in range(len(df_vital_sorted) - window_size):
                # 特征窗口
                window_features = []
                for j in range(window_size):
                    row = df_vital_sorted.iloc[i + j]
                    window_features.extend([
                        row.get('temperature', 36.5),
                        row.get('blood_pressure_systolic', 120),
                        row.get('blood_pressure_diastolic', 80),
                        row.get('heart_rate', 70),
                        row.get('respiratory_rate', 16),
                        row.get('oxygen_saturation', 98)
                    ])
                
                # 目标值（下一个时间点的生命体征）
                target_row = df_vital_sorted.iloc[i + window_size]
                target = [
                    target_row.get('temperature', 36.5),
                    target_row.get('blood_pressure_systolic', 120),
                    target_row.get('blood_pressure_diastolic', 80),
                    target_row.get('heart_rate', 70),
                    target_row.get('respiratory_rate', 16),
                    target_row.get('oxygen_saturation', 98)
                ]
                
                features.append(window_features)
                targets.append(target)
            
            X = np.array(features)
            y = np.array(targets)
            
            # 特征标准化
            scaler_X = StandardScaler()
            scaler_y = StandardScaler()
            
            X_scaled = scaler_X.fit_transform(X)
            y_scaled = scaler_y.fit_transform(y)
            
            # 分割数据
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y_scaled, test_size=0.2, random_state=42
            )
            
            # 创建LSTM模型用于时间序列预测
            model = Sequential([
                LSTM(64, return_sequences=True, input_shape=(window_size, 6)),
                Dropout(0.2),
                LSTM(32, return_sequences=False),
                Dropout(0.2),
                Dense(16, activation='relu'),
                Dense(6)  # 6个输出特征
            ])
            
            model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
            
            # 重塑数据为LSTM格式
            X_train_reshaped = X_train.reshape(-1, window_size, 6)
            X_test_reshaped = X_test.reshape(-1, window_size, 6)
            
            # 训练模型
            early_stopping = EarlyStopping(patience=10, restore_best_weights=True)
            
            history = model.fit(
                X_train_reshaped, y_train,
                validation_data=(X_test_reshaped, y_test),
                epochs=100,
                batch_size=32,
                callbacks=[early_stopping],
                verbose=0
            )
            
            # 评估模型
            y_pred_scaled = model.predict(X_test_reshaped)
            y_pred = scaler_y.inverse_transform(y_pred_scaled)
            y_test_orig = scaler_y.inverse_transform(y_test)
            
            # 计算评估指标
            mse = mean_squared_error(y_test_orig, y_pred)
            mae = mean_absolute_error(y_test_orig, y_pred)
            r2 = r2_score(y_test_orig.flatten(), y_pred.flatten())
            
            # 保存模型
            self.save_model(model, 'vital_signs_predictor', 'lstm')
            self.save_preprocessor(scaler_X, 'vital_scaler_X')
            self.save_preprocessor(scaler_y, 'vital_scaler_y')
            
            print(f"生命体征预测模型 - MSE: {mse:.4f}, MAE: {mae:.4f}, R2: {r2:.4f}")
            
            return {
                'mse': mse,
                'mae': mae,
                'r2': r2,
                'history': history.history
            }
            
        except Exception as e:
            print(f"生命体征预测模型训练错误: {e}")
            return None
    
    def train_patient_clustering(self):
        """训练患者聚类模型"""
        try:
            print("开始训练患者聚类模型...")
            
            # 加载数据
            df_medical, df_vital, df_maternal = self.load_and_prepare_data()
            if df_medical is None:
                return None
            
            # 准备特征数据
            X, _ = self.prepare_medical_features(df_medical, df_vital)
            if X is None:
                return None
            
            # 特征标准化
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # 尝试不同的聚类数量
            cluster_range = range(2, 11)
            silhouette_scores = []
            calinski_scores = []
            
            for n_clusters in cluster_range:
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                cluster_labels = kmeans.fit_predict(X_scaled)
                
                silhouette_avg = silhouette_score(X_scaled, cluster_labels)
                calinski_avg = calinski_harabasz_score(X_scaled, cluster_labels)
                
                silhouette_scores.append(silhouette_avg)
                calinski_scores.append(calinski_avg)
            
            # 选择最佳聚类数量
            best_n_clusters = cluster_range[np.argmax(silhouette_scores)]
            
            # 训练最终模型
            final_kmeans = KMeans(n_clusters=best_n_clusters, random_state=42)
            cluster_labels = final_kmeans.fit_predict(X_scaled)
            
            # 分析聚类结果
            cluster_analysis = {}
            for i in range(best_n_clusters):
                cluster_mask = cluster_labels == i
                cluster_data = X_scaled[cluster_mask]
                
                cluster_analysis[f'cluster_{i}'] = {
                    'size': len(cluster_data),
                    'percentage': len(cluster_data) / len(X_scaled) * 100,
                    'center': final_kmeans.cluster_centers_[i].tolist()
                }
            
            # 保存模型
            self.save_model(final_kmeans, 'patient_clustering', 'kmeans')
            self.save_preprocessor(scaler, 'clustering_scaler')
            
            print(f"患者聚类完成，最佳聚类数: {best_n_clusters}")
            
            return {
                'best_n_clusters': best_n_clusters,
                'silhouette_scores': silhouette_scores,
                'calinski_scores': calinski_scores,
                'cluster_analysis': cluster_analysis,
                'cluster_labels': cluster_labels.tolist()
            }
            
        except Exception as e:
            print(f"患者聚类模型训练错误: {e}")
            return None
    
    def predict_disease(self, patient_data):
        """预测疾病类别"""
        try:
            # 加载模型和预处理器
            model = self.load_model('disease_classifier')
            scaler = self.load_preprocessor('disease_scaler')
            encoder = self.load_preprocessor('disease_encoder')
            
            if model is None or scaler is None or encoder is None:
                return None
            
            # 准备特征
            features = self.extract_patient_features(patient_data)
            features_scaled = scaler.transform([features])
            
            # 预测
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(features_scaled)[0]
                prediction = model.predict(features_scaled)[0]
            else:
                # 神经网络
                predictions = model.predict(features_scaled)[0]
                probabilities = predictions
                prediction = np.argmax(predictions)
            
            # 解码标签
            disease_name = encoder.inverse_transform([prediction])[0]
            
            # 创建结果
            result = {
                'predicted_disease': disease_name,
                'confidence': float(max(probabilities)),
                'all_probabilities': {
                    encoder.inverse_transform([i])[0]: float(prob) 
                    for i, prob in enumerate(probabilities)
                }
            }
            
            return result
            
        except Exception as e:
            print(f"疾病预测错误: {e}")
            return None
    
    def predict_vital_signs(self, historical_data):
        """预测生命体征"""
        try:
            # 加载模型和预处理器
            model = self.load_model('vital_signs_predictor')
            scaler_X = self.load_preprocessor('vital_scaler_X')
            scaler_y = self.load_preprocessor('vital_scaler_y')
            
            if model is None or scaler_X is None or scaler_y is None:
                return None
            
            # 准备时间序列数据
            features = []
            for record in historical_data[-3:]:  # 使用最近3条记录
                features.extend([
                    record.get('temperature', 36.5),
                    record.get('blood_pressure_systolic', 120),
                    record.get('blood_pressure_diastolic', 80),
                    record.get('heart_rate', 70),
                    record.get('respiratory_rate', 16),
                    record.get('oxygen_saturation', 98)
                ])
            
            # 标准化和预测
            features_scaled = scaler_X.transform([features])
            features_reshaped = features_scaled.reshape(-1, 3, 6)
            
            prediction_scaled = model.predict(features_reshaped)
            prediction = scaler_y.inverse_transform(prediction_scaled)
            
            # 创建结果
            result = {
                'predicted_temperature': float(prediction[0][0]),
                'predicted_blood_pressure_systolic': float(prediction[0][1]),
                'predicted_blood_pressure_diastolic': float(prediction[0][2]),
                'predicted_heart_rate': float(prediction[0][3]),
                'predicted_respiratory_rate': float(prediction[0][4]),
                'predicted_oxygen_saturation': float(prediction[0][5])
            }
            
            return result
            
        except Exception as e:
            print(f"生命体征预测错误: {e}")
            return None
    
    def get_patient_cluster(self, patient_data):
        """获取患者聚类信息"""
        try:
            # 加载模型和预处理器
            model = self.load_model('patient_clustering')
            scaler = self.load_preprocessor('clustering_scaler')
            
            if model is None or scaler is None:
                return None
            
            # 准备特征
            features = self.extract_patient_features(patient_data)
            features_scaled = scaler.transform([features])
            
            # 预测聚类
            cluster = model.predict(features_scaled)[0]
            
            return {
                'cluster_id': int(cluster),
                'cluster_name': f'患者群组_{cluster}'
            }
            
        except Exception as e:
            print(f"患者聚类错误: {e}")
            return None
    
    def extract_patient_features(self, patient_data):
        """提取患者特征"""
        features = [
            patient_data.get('hospital_id', 0),
            patient_data.get('department_id', 0),
            patient_data.get('visit_type', 0),
            patient_data.get('temperature', 36.5),
            patient_data.get('blood_pressure_systolic', 120),
            patient_data.get('blood_pressure_diastolic', 80),
            patient_data.get('heart_rate', 70),
            patient_data.get('respiratory_rate', 16),
            patient_data.get('oxygen_saturation', 98)
        ]
        
        # 时间特征
        if 'visit_date' in patient_data:
            visit_date = pd.to_datetime(patient_data['visit_date'])
            features.extend([visit_date.hour, visit_date.dayofweek, visit_date.month])
        else:
            features.extend([12, 1, 1])
        
        # 衍生特征
        systolic = patient_data.get('blood_pressure_systolic', 120)
        diastolic = patient_data.get('blood_pressure_diastolic', 80)
        pulse_pressure = systolic - diastolic
        map_pressure = diastolic + pulse_pressure / 3
        features.extend([pulse_pressure, map_pressure])
        
        # 体温分类
        temp = patient_data.get('temperature', 36.5)
        if temp > 37.5:
            temp_category = 2
        elif temp < 36.0:
            temp_category = 0
        else:
            temp_category = 1
        features.append(temp_category)
        
        return features
    
    def get_feature_names(self):
        """获取特征名称"""
        return [
            'hospital_id', 'department_id', 'visit_type',
            'temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'heart_rate', 'respiratory_rate', 'oxygen_saturation',
            'visit_hour', 'visit_dayofweek', 'visit_month',
            'pulse_pressure', 'mean_arterial_pressure', 'temperature_category'
        ]
    
    def save_model(self, model, model_name, model_type):
        """保存模型"""
        try:
            if model_type == 'neural_network' or model_type == 'lstm':
                model_path = os.path.join(self.model_dir, f"{model_name}.h5")
                model.save(model_path)
            else:
                model_path = os.path.join(self.model_dir, f"{model_name}.joblib")
                joblib.dump(model, model_path)
            
            # 保存模型类型信息
            info_path = os.path.join(self.model_dir, f"{model_name}_info.json")
            with open(info_path, 'w') as f:
                json.dump({'type': model_type}, f)
                
        except Exception as e:
            print(f"模型保存错误: {e}")
    
    def load_model(self, model_name):
        """加载模型"""
        try:
            info_path = os.path.join(self.model_dir, f"{model_name}_info.json")
            if not os.path.exists(info_path):
                return None
            
            with open(info_path, 'r') as f:
                info = json.load(f)
            
            model_type = info['type']
            
            if model_type == 'neural_network' or model_type == 'lstm':
                model_path = os.path.join(self.model_dir, f"{model_name}.h5")
                if os.path.exists(model_path):
                    return load_model(model_path)
            else:
                model_path = os.path.join(self.model_dir, f"{model_name}.joblib")
                if os.path.exists(model_path):
                    return joblib.load(model_path)
            
            return None
            
        except Exception as e:
            print(f"模型加载错误: {e}")
            return None
    
    def save_preprocessor(self, preprocessor, name):
        """保存预处理器"""
        try:
            path = os.path.join(self.model_dir, f"{name}.joblib")
            joblib.dump(preprocessor, path)
        except Exception as e:
            print(f"预处理器保存错误: {e}")
    
    def load_preprocessor(self, name):
        """加载预处理器"""
        try:
            path = os.path.join(self.model_dir, f"{name}.joblib")
            if os.path.exists(path):
                return joblib.load(path)
            return None
        except Exception as e:
            print(f"预处理器加载错误: {e}")
            return None
    
    def train_all_models(self):
        """训练所有模型"""
        print("开始训练所有机器学习模型...")
        
        results = {}
        
        # 训练疾病分类模型
        disease_result = self.train_disease_classification_model()
        results['disease_classification'] = disease_result
        
        # 训练生命体征预测模型
        vital_result = self.train_vital_signs_prediction()
        results['vital_signs_prediction'] = vital_result
        
        # 训练患者聚类模型
        cluster_result = self.train_patient_clustering()
        results['patient_clustering'] = cluster_result
        
        print("所有模型训练完成！")
        return results