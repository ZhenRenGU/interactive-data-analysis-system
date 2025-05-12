import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import json

# 这里可以实现机器学习模型相关的函数 

def linear_regression(df, features, target, test_size=0.2, random_state=42):
    """
    执行线性回归分析
    
    参数:
    df (DataFrame): 数据集
    features (list): 特征列名列表
    target (str): 目标列名
    test_size (float): 测试集比例
    random_state (int): 随机种子
    
    返回:
    dict: 包含模型结果的字典
    """
    # 提取特征和目标变量
    X = df[features]
    y = df[target]
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # 创建线性回归模型
    model = LinearRegression()
    
    # 训练模型
    model.fit(X_train, y_train)
    
    # 预测
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # 评估模型
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    
    # 获取系数和截距
    coefficients = {features[i]: float(model.coef_[i]) for i in range(len(features))}
    intercept = float(model.intercept_)
    
    # 准备散点图数据
    plot_data = []
    for i, feature in enumerate(features):
        plot_data.append({
            'feature': feature,
            'coefficient': float(model.coef_[i]),
            'x_train': X_train[feature].tolist(),
            'y_train': y_train.tolist(),
            'x_test': X_test[feature].tolist(),
            'y_test': y_test.tolist()
        })
    
    # 返回结果
    result = {
        'coefficients': coefficients,
        'intercept': intercept,
        'metrics': {
            'train_rmse': float(train_rmse),
            'test_rmse': float(test_rmse),
            'train_r2': float(train_r2),
            'test_r2': float(test_r2)
        },
        'feature_importance': {feature: abs(coef) for feature, coef in coefficients.items()},
        'equation': f"{target} = {' + '.join([f'{coef:.4f} * {feat}' for feat, coef in coefficients.items()])} + {intercept:.4f}",
        'plot_data': plot_data
    }
    
    return result 