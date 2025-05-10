from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
from werkzeug.utils import secure_filename
import json
app = Flask(__name__)
CORS(app)  # 允许跨域请求


#配置文件上传存储路径
UPLOAD_FOLDER = 'static/uploads'

#如果文件夹不存在，则创建文件夹
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#配置文件上传存储路径
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#允许的文件扩展名
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'
                      }

#判断文件是否允许上传
def allowed_file(filename):
    #判断文件后缀是否在允许的文件扩展名列表中
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#文件上传接口
@app.route('/api/upload',methods=['POST'])
def upload_file():
    #判断是否选择文件
    if 'file' not in request.files:
        return jsonify({'error': '没有选择文件'}), 400
    
    #获取上传的文件
    file = request.files['file']

    #判断文件是否为空
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    #判断文件是否允许上传
    if not allowed_file(file.filename):
        return jsonify({'error': '文件格式不支持'}), 400
    
    #保存文件
    filename = secure_filename(file.filename)
    #获取文件保存路径
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    #返回文件上传成功信息
    return jsonify({
            'success': True,
            'filename': filename,
            'message': '文件上传成功'
        }), 200


#数据预览接口
@app.route('/api/preview/<filename>',methods=['GET'])
def preview_data(filename):
    #获取文件保存路径
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    #判断文件是否存在
    if not os.path.exists(file_path):
        return jsonify({'error': '文件不存在'}), 404
    
    #根据文件类型读取数据
    if filename.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        df = pd.read_excel(file_path)
    else:
        return jsonify({'error': '文件格式不支持'}), 400
    
    #获取基本信息
    info = {
        'rows': len(df),  #行数
        'columns': len(df.columns),  #列数
        'column_names': df.columns.tolist(),  #列名
        'dtypes': df.dtypes.astype(str).to_dict(),  #数据类型
        'missing_values': df.isnull().sum().to_dict(),  #缺失值
        'preview': json.loads(df.head(10).to_json(orient='records'))  #预览数据
    }

    #返回基本信息
    return jsonify({
        'success': True,
        'info': info
    }), 200


#获取文件列表
@app.route('/api/files',methods=['GET'])
def get_files():
    #获取文件夹中的所有文件
    files=[]
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(filename):
            files.append(filename)
    #返回文件列表
    return jsonify({
        'success': True,
        'files': files
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
