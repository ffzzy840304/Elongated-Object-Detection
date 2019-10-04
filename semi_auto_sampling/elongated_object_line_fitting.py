# -*- coding: utf-8 -*-
"""
Created on Fri Aug 03 13:29:44 2018

@author: User
"""

from __future__ import division
import sys
import os
import cv2
import math


def linefit(x , y):
    N = float(len(x))
    sx,sy,sxx,syy,sxy=0,0,0,0,0
    for i in range(0,int(N)):
        sx  += x[i]
        sy  += y[i]
        sxx += x[i]*x[i]
        syy += y[i]*y[i]
        sxy += x[i]*y[i]
    if(sx*sx/N -sxx)==0:
       return -10000
    else:
       a = (sy*sx/N -sxy)/( sx*sx/N -sxx)
       b = (sy - a*sx)/N
       return a,b
def Ave(x):
    r=0.0
    for i in x:
        r+=i
    result=r/len(x)
    return result

dir_map='G:\\coco\\annotations\\downloads\\train2017\\'
dir_file='G:\\coco\\statistic\\training_groundtruth\\80.txt'

f=open(dir_file)
lines=f.readlines()
for line in lines:
    line=line.strip('\n')
    index1=line.find(' ')
    index2=line.find(' ',index1+1)
    index3=line.find(' ',index2+1)
    index4=line.find(' ',index3+1)
    index5=line.find(' ',index4+1)
    #index6=line.find(' ',index5+1)
    imagename=str(line[:index1]).zfill(12)+'.png'
    imagename_jpg=str(line[:index1]).zfill(12)+'.jpg'
     
    xmin=int(float(line[index2+1:index3]))
    ymin=int(float(line[index3+1:index4]))
    xmax=int(float(line[index4+1:index5]))
    ymax=int(float(line[index5+1:]))
    img=cv2.imread(dir_map+imagename,0)
    
    cv2.imwrite('G:\\coco\\statistic\\narrow_object_line_fitting\\toothbrush\\map_train\\'+imagename,img)
   # img_jpg=cv2.imread('G:\\coco\\statistic\\narrow_object_line_fitting\\baseball_bat\\'+imagename_jpg)
    im_black=cv2.imread('G:\\coco\\statistic\\narrow_object_line_fitting\\toothbrush\\label_image_train\\'+imagename_jpg)
    
    rows,cols=img.shape    
    
    count=0
    X=[]
    Y=[]
   
    for i in range(rows):
     for j in range(cols):
         if i>=ymin and i<=ymax and j>=xmin and j<=xmax:
             if img[i,j]==89:
               X.append(j)
               Y.append(i)
               
    
    if len(X)>0:
       if(linefit(X,Y)==-10000):
         print imagename
         continue
       a,b=linefit(X,Y)
       if a==0:
           start_point=(xmin,int((ymin+ymax)/2))
           end_point=(xmax,int((ymin+ymax)/2))
       else:
            inter_point=[]
            p1=(xmin,int(a*xmin+b))
            inter_point.append([xmin,int(a*xmin+b)])
            p2=(xmax,int(a*xmax+b))
            inter_point.append([xmax,int(a*xmax+b)])
            p3=(int((ymin-b)/a),ymin)
            inter_point.append([int((ymin-b)/a),ymin])
            p4=(int((ymax-b)/a),ymax)   
            inter_point.append([int((ymax-b)/a),ymax])
            inter_point.sort(key=lambda x:x[0])
            start_point=(inter_point[1][0],inter_point[1][1])
            end_point=(inter_point[2][0],inter_point[2][1])
       #cv2.line(img_jpg,start_point,end_point,(0,0,255),3)
       cv2.line(im_black,start_point,end_point,(255,255,255),3)
      # cv2.imwrite('G:\\coco\\statistic\\narrow_object_line_fitting\\baseball_bat\\'+imagename_jpg,img_jpg)
       cv2.imwrite('G:\\coco\\statistic\\narrow_object_line_fitting\\toothbrush\\label_image_train\\'+imagename_jpg,im_black)
       #print a,b   
      
          
    