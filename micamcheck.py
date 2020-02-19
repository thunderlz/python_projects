#视频监控文件确认，如果出现没有传的情况就体现出来。
import glob
from datetime import datetime
from datetime import timedelta
import pandas as pd
diskpath='/mnt/data1/micam/xiaomi_camera_videos'
with open(diskpath+'/log.txt','at') as logf:
    logf.write('检查时间：'+datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒\n'))
    micams=glob.glob(diskpath+'/5ce50*')
    logf.write('一共有{}个摄像头数据\n'.format(len(micams)))
    for micam in micams:
        mdic={}
        dirs=glob.glob(micam+'/2020*')
        for dir in dirs:
            mdic[dir.split('/')[-1]]=glob.glob(dir+'/*.mp4')
        logf.write('摄像头{}有{}个文件夹，{}个视频\n'.format(micam.split('/')[-1],len(mdic),sum([len(mdic[key]) for key in mdic.keys()])))
        start=(datetime.now()-timedelta(6)).strftime('%Y%m%d')
        keys=[h.strftime('%Y%m%d%H') for h in pd.date_range(start=start,periods=120,freq='H')]
        for key in keys:
      #      print(' {}有{}个文件'.format(key,len(mdic[key])))
            if len(mdic[key]) != 60:
                logf.write('过去5天中，{}异常!!!!!!!!!!!!!\n'.format(key))

