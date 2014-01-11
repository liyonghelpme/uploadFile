# -*- coding: utf-8 -*-
import os
from PIL import Image
import sys
import MySQLdb
import sys
fname = sys.argv[1]

dbHost="192.168.3.105"
dbPasswd = "badperson"
dbName = "qishituan"

TPCommand = "G:/texturepacker/bin/TexturePacker"
if not os.path.exists('gres'):
    os.mkdir('gres')
if not os.path.exists('gtres'):
    os.mkdir('gtres')

#grass tile
#pack as grassOne.plist
im = Image.open(fname)
for i in xrange(0, 4):
    row = i/8
    col = i%8
    nim = Image.new('RGBA', (512, 512))
    oy = row*512
    ox = col*512
    print ox, oy
    cim = im.crop((ox, oy, ox+512, oy+512))
    nim.paste(cim, (0, 0, 512, 512))
    nim.save('gres/grass%d.png' % (i))

cmd = TPCommand + " --smart-update --format cocos2d --data %s\\%s.plist --sheet %s\\%s.png --dither-none-nn --opt RGBA8888 --trim --scale %f %s" % ('gtres', 'grassOne', 'gtres', 'grassOne', 1, 'gres')
os.system(cmd)
#os.system('cp tres/t512.png Z:\\code')
#os.system('cp tres/t512.plist Z:\\code')
import zipfile
import hashlib

os.system('cp gtres/grassOne* .')
zipFile = zipfile.ZipFile('test.zip', 'w')
zipFile.write('grassOne.png')
zipFile.write('grassOne.plist')
zipFile.write('t512.png')
zipFile.write('t512.plist')
zipFile.close()

m = hashlib.md5()
f = open('test.zip').read()
m.update(f)
nf = open('version', 'w')
nf.write(m.hexdigest())
nf.close()

import time
now = time.strftime("%Y%m%d%H%M%S", time.localtime())
os.system('cp z:\\code\\test.zip z:\\code\\test.zip-%s'%(now))
os.system('cp z:\\code\\version z:\\code\\version-%s'%(now))
os.system('cp test.zip Z:\\code')
os.system('cp version Z:\\code')
