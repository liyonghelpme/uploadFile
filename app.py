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
def upload():
    if request.method == 'GET':
        return render_template("upload.html")
    else:
        centerx = request.form.get('centerx', 100, type=int)
        centery = request.form.get('centery', 100, type=int)
        bloodHeight = request.form.get('bloodHeight', 100, type=int)

        f = request.files["file"]
        fname = secure_filename(f.filename)
        f.save(fname)
        if fname[-4:] == '.zip':
            if os.path.exists('temp'):
                os.system('rm -rf temp')
            os.system('mkdir temp')
            os.system('mkdir temp/results')
            os.system('unzip %s -d temp' % (fname))
            os.system('cp packageRole.py temp/')

            name = os.listdir('temp')
            os.chdir('temp')
            print("before package")
            for i in name:
                if os.path.isdir(i):
                    os.system('python packageRole.py %s %d %d %d' % (i, centerx, centery, bloodHeight))    
                    #调用192.168.3.105:9999 的打包接口
                    
                    response = requests.post('http://192.168.3.105:9999/', files={'file':open(os.path.join('results', i+'.png'), 'rb'), 'description':'pic'})
                    print response.content

                    response = requests.post('http://192.168.3.105:9999/', files={'file':open(os.path.join('results', i+'.plist'), 'rb'), 'description':'plist'})
                    print response.content
                
            os.chdir('..')
        return 'successfully upload pictures!!'

if __name__ == '__main__':
    app.run(debug=True, port=9999, host='0.0.0.0')
