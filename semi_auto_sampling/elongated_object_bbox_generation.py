# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random

class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

    def shift(self, x, y):
        self.x += x
        self.y += y

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])
    
def Objectwidth(im):
    #im=cv2.imread(imagename,0)
    ret, im = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
 
    skel = np.zeros(im.shape, np.uint8)
    erode = np.zeros(im.shape, np.uint8)
    temp = np.zeros(im.shape, np.uint8)
 
    c = 0
    while True:
	    #cv2.imshow('im %d'%(i), im)
	    erode = cv2.erode(im,element)
	    temp  = cv2.dilate(erode, element)
 
	    
	    temp = cv2.subtract(im, temp)
	    #cv2.imshow('skeleton part %d' %(i,), temp)
	    skel = cv2.bitwise_or(skel, temp)
	    im = erode.copy()
	    c=c+1
	    if cv2.countNonZero(im)== 0:
		    break;
       
    #print c-1
    return c-1

#dir_size='G:\\coco\\statistic\\narrow_object_line_fitting\\toothbrush\\bbox_size\\val\\8'
dir_label='G:\\elongated_project\\FF\\adaptive_sampling\\labels\\'
dir_source='G:\\elongated_project\\FF\\adaptive_sampling\\images\\'
dir_txt='G:\\elongated_project\\FF\\adaptive_sampling\\txt_bbox\\'

imagelist=[]
sourceimage_list=[]

filenames=os.listdir(dir_label)
for fn in filenames:
    fullfilename=os.path.join(dir_label,fn)
    if fullfilename[-3:]=='jpg':
        imagelist.append(fullfilename)


filenames=os.listdir(dir_source)
for fn in filenames:
    fullfilename=os.path.join(dir_source,fn)
    if fullfilename[-3:]=='jpg':
        sourceimage_list.append(fullfilename)


object_pixels=[]
#nonobject_pixels=[]
for k in range(0,len(imagelist)):
    index=imagelist[k].rfind('\\')
    print imagelist[k]
    img=cv2.imread(dir_label+imagelist[k][index+1:],0)    
    src_img=cv2.imread(dir_source+imagelist[k][index+1:])
    #set bouding box radius based on calculated object width
    width=Objectwidth(img)
    r=int(width*1.2)+15
    print r
    rows,cols=img.shape
    for i in range (rows):
        for j in range (cols):
            p=Point(j,i)
            if(img[i,j]>128):                
                object_pixels.append(p) 
                img[i,j]=255
            
    random.shuffle(object_pixels)
    #random.shuffle(nonobject_pixels)    

    seg_num=round(len(object_pixels)/width)
    object_seg=[]
    #nonobject_seg=[]
    seg_count=0
    for i in range(0,len(object_pixels)):
        if seg_num==0:
            break;
        px=object_pixels[i].x
        py=object_pixels[i].y
        if(px>=r)and(px<=(cols-r))and(py>=r)and(py<=(rows-r)):
            object_seg.append(object_pixels[i])
            seg_count=seg_count+1
            if(seg_count==seg_num):
                break
           
    seg_num=round(len(object_pixels)/2)
    seg_count=0
   
    #do crop now
   
    index=imagelist[k].rfind('\\')
    txt_savename=dir_txt+imagelist[k][index+1:-3]+'txt'
    new_img=src_img.copy()
    seg_count=0
    
    for pix in object_seg:
        crop_img=img[pix.y-r:pix.y+r,pix.x-r:pix.x+r]
        crop_srcimg=src_img[pix.y-r:pix.y+r,pix.x-r:pix.x+r]        
        cv2.rectangle(new_img,(pix.x-r,pix.y-r),(pix.x+r,pix.y+r),(0,0,255),1)
        
        fsave=open(txt_savename,'a+')
        fsave.writelines(str(pix.x-r)+' '+str(pix.y-r)+' '+str(pix.x+r)+' '+str(pix.y+r)+' '+'baseball_bat')
        fsave.writelines('\n')
        fsave.close()
        
        seg_count=seg_count+1      

        
    #to check whether object patch cropping correct or not
    cv2.imwrite('G:\\elongated_project\\FF\\adaptive_sampling\\source_bb\\'+imagelist[k][index+1:],new_img)
    
    print 'done' 
    object_pixels[:]=[]
    #nonobject_pixels[:]=[]
   

print 'all croping done'
      
