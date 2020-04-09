import glob
import numpy as np
import cv2
import datetime
import os
# import fnmatch
# import re
import subprocess


def fileProcessing(file_list):
    print("start----------------")
    codePre = "ffmpeg -threads 2 -i "
    # codeMid = " -vcodec h264 "
    # codeMid = " -vcodec libx264 -acodec aac -preset fast -b:v 2000k "
    # codeMid = " -vcodec libx264 -acodec aac "
    codeMid = ' -vcodec h264 -an -s 1920x1080 '
    for file_path in file_list:
        subname = file_path.split('.')
        print(subname)
        output_path = subname[0] + "_new.mp4"   # 处理后的文件路径
        command = codePre + file_path + codeMid + output_path
        print(command)
        file_name = os.path.basename(file_path).split('.')
        # result = os.system(command)
        # if(result != 0):
        #     gl_failed_list.append(file_path)
        #     print(file_name[0], "is failed-----", "result = ", result)
        # else:
        #     print("end------", file_name[0], "result = ", result)

        try:
            retcode = subprocess.call(command, shell=True)
            if retcode == 0:
                print(file_name[0], "successed------")
            else:
                print(file_name[0], "is failed--------")
        except Exception as e:
            print("Error:", e)

    print("---------------End all-----------------")
    # print("failed:", gl_failed_list)


# 获取文件名并排序
# vpath='/Volumes/micamsdir/xiaomi_camera_videos/5ce50c74d629/'
vpath = '/Volumes/micamsdir/xiaomi_camera_videos/5ce50c581545/'
vpathlist = []
for vdir in glob.glob(vpath+'*'):
    vpathlist.extend(glob.glob(vdir+'/*'))
vpathlist.sort()
print(len(vpathlist))
print(vpathlist[-1][53:70])

# 每个文件取第一帧
start = (datetime.datetime.now()-datetime.timedelta(1)).strftime('%Y%m%d')+'00'
end = (datetime.datetime.now()-datetime.timedelta(1)).strftime('%Y%m%d')+'24'
ndvideo = []
dim = (900, 540)
printctl = 0
for vfile in vpathlist:
    if vfile[53:63] >= start and vfile[53:63] <= end:
        if printctl % 10 == 0:
            print(vfile[53:70])
        printctl += 1
        cap = cv2.VideoCapture(vfile)
        ret, img_nd = cap.read()
        img_nd = cv2.resize(img_nd, dim)
#         img_nd=denoise(img_nd,1)
#         img_nd=cv2.equalizeHist(img_nd)
        ndvideo.append(img_nd)

        # 输出视频
# fourcc = cv2.VideoWriter_fourcc(*'H264')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/Users/leizhen/windowvideo.mp4',
                      fourcc, 25.0, dim, True)
for i in ndvideo:
    out.write(i)
out.release()

filelist = ['/Users/leizhen/windowvideo.mp4']
fileProcessing(filelist)
