import pandas as pd
import numpy as np

# 这里可以实现数据清洗的函数 

#处理缺失值
def handle_missing_values(df,strategy,columns=None,fill_value=None):
    """
    处理缺失值
    
    参数:
    df (DataFrame): 待处理的数据集
    strategy (str): 处理策略，可选 'drop', 'mean', 'median', 'mode', 'value'
    columns (list): 要处理的列，默认为所有列
    fill_value: 当strategy为'value'时使用的填充值
    
    返回:
    DataFrame: 处理后的数据集
    """

    if strategy not in ['drop', 'mean', 'median', 'mode', 'value']:
        raise ValueError("Invalid strategy!")
    if strategy == 'value' and fill_value is None:
        raise ValueError("fill_value must be provided when strategy='value'")

    #如果columns为None，则处理所有列
    if columns is None:
        columns = df.columns
    
    #创建一个副本
    df_clean=df.copy()

    #根据策略处理缺失值
    if strategy == 'drop':
        df_clean=df_clean.dropna(subset=columns)
    else:
        for col in columns:
            if col in df_clean.columns:
                if pd.api.types.is_numeric_dtype(df_clean[col]):
                    if strategy == 'mean':
                        df_clean[col]=df_clean[col].fillna(df_clean[col].mean())
                    elif strategy == 'median':
                        df_clean[col]=df_clean[col].fillna(df_clean[col].median())
                    elif strategy == 'mode':
                        df_clean[col]=df_clean[col].fillna(df_clean[col].mode()[0])
                    elif strategy == 'value':
                        df_clean[col]=df_clean[col].fillna(fill_value)
                else: #如果是非数值类型
                    if strategy == 'value':
                        df_clean[col]=df_clean[col].fillna(fill_value)
                    else:
                        df_clean[col]=df_clean[col].fillna(df_clean[col].mode()[0])
    return df_clean


#检测异常值
def detect_outliers(df,method='zscore',columns=None,threshold=3):
    """
    检测异常值
    
    参数:
    df (DataFrame): 待处理的数据集
    method (str): 检测方法，可选 'zscore', 'iqr'
    columns (list): 要处理的列，默认为所有数值列
    threshold (float): 阈值，Z-score方法使用
    
    返回:
    dict: 包含每列异常值索引的字典
    """
     
    #如果columns为None，则处理所有数值列
    if columns is None:
        columns=df.select_dtypes(include=[np.number]).columns
    
    #创建一个字典来存储每列的异常值索引
    outliers={}

    #遍历每列
    for col in columns:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            if method == 'zscore':
                #计算z-score
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                #找到异常值
                outliers[col]=df.index[z_scores>threshold].tolist()
            elif method == 'iqr':
                #计算四分位数
                q1=df[col].quantile(0.25)
                q3=df[col].quantile(0.75)
                iqr=q3-q1
                #找到异常值
                outliers[col]=df.index[(df[col]<q1-1.5*iqr) | (df[col]>q3+1.5*iqr)].tolist()
    return outliers

#删除异常值
def remove_outliers(df,outliers):
    """
    删除异常值
    
    参数:
    df (DataFrame): 待处理的数据集
    outliers (dict): 包含每列异常值索引的字典
    
    返回:
    DataFrame: 处理后的数据集
    """
    
    #创建一个副本
    df_clean=df.copy()

    #获取所需要删除的行索引
    all_indices=[]
    for col,indices in outliers.items():
        all_indices.extend(indices)

    #删除异常值所在行
    df_clean=df_clean.drop(index=list(set(all_indices)))

    #打印删除的行数用于调试
    print(f"删除了 {len(set(all_indices))} 行,
          占比为{len(set(all_indices)) / len(df):.1%}).")
          
    #返回处理后的数据集
    return df_clean

#数据标准化
def normalize_data(df,method='minmax',columns=None):
    """
    数据标准化/归一化
    
    参数:
    df (DataFrame): 待处理的数据集
    method (str): 处理方法，可选 'minmax', 'zscore'
      (minmax : 最小最大归一化，值域【0-1】; zscore : 标准化，均值为0，标准差为1)
    columns (list): 要处理的列，默认为所有数值列
    
    返回:
    DataFrame: 处理后的数据集
    """
    
    #如果columns为None，则处理所有数值列
    if columns is None:
        columns=df.select_dtypes(include=[np.number]).columns.tolist()
    
    #创建一个副本
    df_normalized=df.copy()
    
    for col in columns:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            if method == 'minmax':
                #计算最小值和最大值
                min_val=df[col].min()
                max_val=df[col].max()
                #归一化
                if max_val > min_val:
                    df_normalized[col]=(df[col]-min_val)/(max_val-min_val)
            elif method == 'zscore':
                #计算均值和标准差
                mean=df[col].mean()
                std=df[col].std()
                #标准化
                if std > 0: 
                    df_normalized[col]=(df[col]-mean)/std

    return df_normalized


