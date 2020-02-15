import glob
import numpy as np
import cv2
import datetime

def denoise(img,n=1):
    for i in range(n):
        if i==0:
            mid=img
        mid=cv2.fastNlMeansDenoisingColored(mid,None,10,10,7,21)
    dst=mid
    return dst

#获取文件名并排序
import glob
homepath='/mnt/data1'
vpaths=[]
vpaths.append(homepath+'/micam/xiaomi_camera_videos/5ce50c581545/')
vpaths.append(homepath+'/micam/xiaomi_camera_videos/5ce50c74d629/')
for vpath in vpaths:
    vpathlist=[]
    #获取所有文件目录
    for vdir in glob.glob(vpath+'*'):
        vpathlist.extend(glob.glob(vdir+'/*'))
    vpathlist.sort()
    print(len(vpathlist))
    print(vpathlist[-1])


    #每个文件取第一帧
    yesterday=(datetime.datetime.now()-datetime.timedelta(1)).strftime('%Y%m%d')
    start=yesterday+'00'
    end=yesterday+'24'
    ndvideo=[]
    dim=(1920,1080)
    printctl=0
    for vfile in vpathlist:
    #    print(vfile[51:61])
        if vfile[51:61]>=start and vfile[51:61]<=end:
            if printctl%10==0:
                print(vfile[51:68])
            printctl+=1
            cap=cv2.VideoCapture(vfile)
            ret,img_nd=cap.read()
            img_nd=cv2.resize(img_nd,dim)
            # img_nd=denoise(img_nd,1)
            ndvideo.append(img_nd)

    # 输出视频
    # fourcc = cv2.VideoWriter_fourcc(*'H264')
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter(vpath+'dist/'+yesterday+'.mp4',fourcc, 15.0, dim,True)
    for i in ndvideo:
        out.write(i)
    out.release()