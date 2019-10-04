# -*- coding: utf-8 -*-
"""
Created on Wed Aug 08 14:22:44 2018

@author: User
"""

import os
import sys
import cv2

dir='G:\\coco\\statistic\\narrow_object_line_fitting\\baseball_bat\\map_val'
dir_file='G:\\coco\\statistic\\validation_groundtruth\\35.txt'

image_name=[]
bbx=[]
f=open(dir_file)
lines=f.readlines()
for line in lines:
    line=line.strip('\n')
    index1=line.find(' ')
    index2=line.find(' ',index1+1)
    index3=line.find(' ',index2+1)
    index4=line.find(' ',index3+1)
    index5=line.find(' ',index4+1)
    index6=line.find(' ',index5+1)
    imagename=str(line[:index1]).zfill(12)+'.png'
    image_name.append(imagename)
    xmin=int(float(line[index3+1:index4]))
    ymin=int(float(line[index4+1:index5]))
    xmax=int(float(line[index5+1:index6]))
    ymax=int(float(line[index6+1:]))
    bbx.append([xmin,ymin,xmax,ymax])
    
image_list=[]
filenames=os.listdir(dir)
for fn in filenames:
    fullfilename=os.path.join(dir,fn)
    if fullfilename[-3:]=='png':
      #index1=fullfilename.rfind('\\')      
      image_list.append(fullfilename)
image_list.sort(key=str.lower)

for i in range(0,len(image_list)):
    im=cv2.imread(image_list[i],0)
    index=image_list[i].rfind('\\') 
    max_p=0
    for j in range(0,len(image_name)):
        if(image_list[i][index+1:]==image_name[j]):
          
          if(bbx[j][2]-bbx[j][0])>=(bbx[j][3]-bbx[j][1]):
              for m in range(bbx[j][0],bbx[j][2]):
                 count=0
                 for n in range(bbx[j][1],bbx[j][3]):
                    if im[n,m]==38:
                        count+=1
                 if(count>max_p):
                   max_p=count             
          elif(bbx[j][2]-bbx[j][0])<(bbx[j][3]-bbx[j][1]):
              for n in range(bbx[j][1],bbx[j][3]): 
                  count=0
                  for m in range(bbx[j][0],bbx[j][2]):
                      if im[n,m]==38:                          
                          count+=1
                  if (count>max_p):
                     max_p=count
    print image_list[i][index+1:],max_p
    fsave=open('G:\\coco\\statistic\\narrow_object_line_fitting\\baseball_bat\\baseball_bat_crop_val_1.txt','a+')
    fsave.writelines(image_list[i][index+1:]+' '+str(max_p)+'\n')
          
                  
    