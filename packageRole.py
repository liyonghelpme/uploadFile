# -*- coding: utf-8 -*-
import os
from PIL import Image
import sys
import MySQLdb

dbHost="192.168.3.105"
dbPasswd = "badperson"
dbName = "qishituan"

TPCommand = "G:/texturepacker/bin/TexturePacker"

def addRoleImages(filepath, ds, minbox, images):
    fdir = os.path.join(filepath, ds)
    flist = sorted(os.listdir(fdir))
    index = 0
    for f in flist:
        if f.split(".")[-1]=="png":
            item = dict()
            item['name'] = '%s_%d.png' % (ds, index)
            index = index+1
            
            im = Image.open(os.path.join(fdir, f))
            box = list(im.getbbox())
            if box[0]<minbox[0]:
                minbox[0] = box[0]
            if box[1]<minbox[1]:
                minbox[1] = box[1]
            if box[2]>minbox[2]:
                minbox[2] = box[2]
            if box[3]>minbox[3]:
                minbox[3] = box[3]
            item['image'] = im
            item['box'] = box
            images.append(item)
    return index

def insertToDb(roleid, nlist, vlist):
    con = MySQLdb.connect(host=dbHost, user='root', passwd=dbPasswd, db=dbName, charset='utf8')
    cur = con.cursor()
    
    alist = []
    blist = []
    for n in nlist:
        alist.append("`%s`=VALUES(`%s`)" % (n,n))
    for v in vlist:
        blist.append(str(v))
    sql = "insert into `knight_view_property` (`id`,`" + ("`,`".join(nlist)) + "`) VALUES (%d,%s) on duplicate key update" % (roleid, ",".join(blist))
    l = len(nlist)
    sql = sql+ ",".join(alist)
    cur.execute(sql)
    con.commit()
    con.close()

#获得这个士兵 基于中心点的最小包围盒子
def packageRole(filepath, cx, cy, height):
    fname = filepath.split("/")[-1]
    dirList = os.listdir(filepath)
    imageList = []
    minbox = [2048, 2048, 0, 0]
    nlist = []
    vlist = []
    scale = 1
    
    for ds in dirList:
        #遍历每个文件夹 dj gj sj zou
        if os.path.isdir(os.path.join(filepath, ds)):
            num = addRoleImages(filepath, ds, minbox, imageList)
            #动画类型
            nlist.append(ds)
            #动画数量
            vlist.append(num)
    resultDir = os.path.join(filepath, "..", "results")
    publishDirName = os.path.join(resultDir, fname)
    if os.path.isdir(publishDirName):
        flist = os.listdir(publishDirName)
        for f in flist:
            os.remove(os.path.join(publishDirName, f))
    else:
        os.system('mkdir %s'%(publishDirName))
        #os.mkdir(publishDirName)

    #每张图片都切割到最小 保存到result目录里面
    for im in imageList:
        nim = im['image'].crop(minbox)
        nim.save("%s/%s_%s" % (publishDirName, fname, im['name']))
    #nlist vlist
    #dj gj sj zou ax ay bh
    #num num num num 

    #ax ay  dj 对齐点 anchorPoint 
    nlist.append('ax')
    vlist.append((cx-minbox[0])*1000/(minbox[2]-minbox[0]))
    nlist.append('ay')
    vlist.append((minbox[3]-cy)*1000/(minbox[3]-minbox[1]))
    nlist.append('bh')
    
    rid = int(fname[4:])
    vlist.append(int(scale*(minbox[3]-height)+0.5))
    #调整数据库 
    insertToDb(rid, nlist, vlist)
    cmd = TPCommand + " --smart-update --format cocos2d --data %s\\%s.plist --sheet %s\\%s.png --dither-none-nn --opt RGBA4444 --trim --disable-rotation --scale %f %s" % (resultDir, fname, resultDir, fname, scale, publishDirName)
    print cmd
    os.system(cmd)

#file path role1
#图片士兵脚底中心对齐点  图片编辑软件中 获取坐标
#血条高度 图片编辑软件中获取坐标
#文件夹格式
#rolexx/ 角色id
#dj gj sj zou 4个文件夹分别放不同的动画图片
#result 图片名称 rolexx_xx_0.png

if len(sys.argv)==5:
    print("packageRole", sys.argv)
    packageRole(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
else:
    print "the command format is python packageRole.py <file-path-name> <centerX> <centerY> <height>\nThe centerX and centerY is the center point in the foot of the roles.\nThe height is the blood height."
