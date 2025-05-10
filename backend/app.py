from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
from werkzeug.utils import secure_filename

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
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'txt', 
                      'json', 'jsonl',
                        'jsonl.gz', 'jsonl.bz2', 'jsonl.zip',
                          'jsonl.tar', 'jsonl.tar.gz', 'jsonl.tar.bz2', 'jsonl.tar.zip'}

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
