import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import json
import base64
from io import BytesIO

# 这里可以实现数据可视化的函数 

def create_line_chart(df, x_column, y_columns, title="折线图", xaxis_title="X轴", yaxis_title="Y轴"):
    """
    创建折线图
    
    参数:
    df (DataFrame): 数据集
    x_column (str): X轴的列名
    y_columns (list): Y轴的列名列表，可以包含多个列用于多条折线
    title (str): 图表标题
    xaxis_title (str): X轴标题
    yaxis_title (str): Y轴标题
    
    返回:
    dict: 包含图表数据的JSON对象
    """
    # 创建图表
    fig = go.Figure()
    
    # 为每个y列添加一条折线
    for col in y_columns:
        fig.add_trace(
            go.Scatter(
                x=df[x_column],
                y=df[col],
                mode='lines+markers',
                name=col
            )
        )
    
    # 设置图表布局
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title="数据系列",
        template="plotly_white"
    )
    
    # 返回JSON格式的图表数据
    return json.loads(fig.to_json())

def create_bar_chart(df, x_column, y_column, title="柱状图", xaxis_title="X轴", yaxis_title="Y轴"):
    """
    创建柱状图 (后续可实现)
    """
    pass

def create_scatter_plot(df, x_column, y_column, title="散点图", xaxis_title="X轴", yaxis_title="Y轴"):
    """
    创建散点图 (后续可实现)
    """
    pass

def export_chart_image(fig, format='png'):
    """
    将图表导出为图片
    
    参数:
    fig (plotly.graph_objects.Figure): 图表对象
    format (str): 图片格式，'png'或'jpeg'
    
    返回:
    str: base64编码的图片数据
    """
    img_bytes = fig.to_image(format=format)
    encoded = base64.b64encode(img_bytes).decode('ascii')
    return f"data:image/{format};base64,{encoded}" 