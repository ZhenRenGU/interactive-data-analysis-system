from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd

app = Flask(__name__)
CORS(app)  # 允许跨域请求

if __name__ == '__main__':
    app.run(debug=True, port=5000)
