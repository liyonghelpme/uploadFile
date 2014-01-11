#coding:utf8
#上传 文件格式
#role1/dj  role1/gj role1/sj role1/zou
#centerx centery bloodHeight

from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
import os
import re
import urllib
import urllib2
import requests

pat = re.compile('role\d+')

app = Flask(__name__, static_url_path="", static_folder="statics")
app.config.from_object(__name__)

#解压缩文件到 temp rolexx 文件夹里面
#
def transFile(cur):
    allF = os.listdir(cur)
    mvFiles = []
    for i in allF:
        fn = os.path.join(cur, i)
        if os.path.isdir(fn):
            transFile(fn)
        elif i.find('.png') != -1:
            os.system('')



@app.route('/', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
#切割图片并且打包
def upload():
    if request.method == 'GET':
        return render_template("tile.html")
    else:
        f = request.files["file"]
        fname = secure_filename(f.filename)
        f.save(fname)
        os.system('python handleTile.py %s' % (fname))
        return 'successfully upload normal tile!!'

@app.route('/uploadGrass', methods=['POST'])
def uploadGrass():
    f = request.files["file"]
    fname = secure_filename(f.filename)
    f.save(fname)
    os.system('python handleGrass.py %s' % (fname))
    return 'successfully upload grass!!'

if __name__ == '__main__':
    app.run(debug=True, port=9999, host='0.0.0.0')
