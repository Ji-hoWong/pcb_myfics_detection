#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 15:28:20 2019

@author: lvhw
"""

import pandas as pd
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from os.path import dirname, abspath


script_dir = dirname(dirname(abspath(__file__)))
print(script_dir)
home = os.path.abspath(script_dir + "/./")
print("home is:",home)
## directory of saving components 组件保存目录
dir_createsave = "/Saving_Extracted_Components/Subset_Microscope"
dir_save = home + dir_createsave
print("dir_save is ", dir_save)
if os.path.exists(dir_save) == 0:
    os.makedirs(dir_save)

            
def extractComponents(sample, csvs, dir_side, intensity="40", \
                                    savecomp=True, check=False):
    print("dir_side is :", dir_side)
    side = dir_side.split("\\")[-1]
    #side = dir_side.split("/")[-1]
    print("side is :",side)
    # rgb = []
    for csv in csvs:
        #print("csv filename: ", csv)
        ## read csv file ;csv文件读取
        annotation_path = os.path.join(dir_side, csv)
        annotation_file = pd.read_csv(annotation_path)
        rgb = ""
        ## read csv content ;阅读csv内容
        img_names = annotation_file["image_name"]          
                    
        img_locations, img_attrs = readAttributes(annotation_file)
        comps_type = img_attrs["type"] 
        comps_text = img_attrs["text"]
        comps_logo = img_attrs["logo"]
        
        prev_name = img_names[0]
        ### read each row for component attributes 读取组件属性的每一行
        for idx in range(0, len(img_names)): 
            img_name = img_names[idx]
            mag = img_name.split("_")[2]
            split_name = img_name.split("_")
            scope_name = ("_").join(split_name[0:3]) + "_" + intensity + \
                                            "_" + ("_").join(split_name[4:]) 
            ## find correspond tif image from image database by name.
            if idx == 0 or img_name != prev_name:
                if img_name != prev_name:
                    if check == True and intensity=="40":
                        dir_comp_save = os.path.join(dir_save, sample, mag)
                        if os.path.exists(dir_comp_save) == 0:
                            os.makedirs(dir_comp_save) 
                    
                        # savepath = os.path.join(dir_comp_save, side)
                        savepath = os.path.join(dir_comp_save, side.split("/")[-1])
                        if os.path.exists(savepath) == 0:
                            os.makedirs(savepath)
                        savename = os.path.join(savepath, prev_name[:-4]+ ".png")
                        # print("labeled image is saved to: ", savename)
                        cv2.imwrite(savename, rgb) 
                        
                # dir_find = os.path.join(home,sample,"Microscope","img",side)
                dir_find = os.path.join(home, sample, "Microscope", "img", side)
                # print("dir_find is:", dir_find)
                img, imgdir = findMicroscopeimg(dir_find, scope_name, side)

                rgb = img.copy()
            
            ## read component shape for polygon, circle, rectangle
            location = img_locations[idx] 
            ### read components property
            comp_type = comps_type[idx]
            
            # ------------------------------------------------#
            # comp_text is the text on the component          #
            # comp_logo is if the component has logo printed  #
            # ------------------------------------------------#
            comp_text = comps_text[idx]
            comp_logo = comps_logo[idx]

            ## extract component from image
            img_comp, rgb = drawbox(location, img, rgb, comp_type)
           
            ## save smd image crop
            if savecomp == True:
                dir_comp_save = os.path.join(dir_save, sample, side, mag)
                if os.path.exists(dir_comp_save) == 0:
                    os.makedirs(dir_comp_save) 
                
                filename = "_".join(".".join(csv.split(".")[:-1]).split("_")[0:3])
                filename = filename + "_" +intensity+"_ring.csv"
                savedir = os.path.join(dir_comp_save, comp_type, filename)
                if os.path.exists(savedir) == 0:
                    os.makedirs(savedir)
                savename = savedir + "/" + comp_type + "_" + str(idx+2) + ".png"
                cv2.imwrite(savename, img_comp)
        
            prev_name = img_name
            
            
        if check == True and intensity=="40":
            dir_comp_save = os.path.join(dir_save, sample, mag)
            if os.path.exists(dir_comp_save) == 0:
                os.makedirs(dir_comp_save) 
        
            savepath = os.path.join(dir_comp_save, side)
            if os.path.exists(savepath) == 0:
                os.makedirs(savepath)
            savename = os.path.join(savepath, prev_name[:-4]+ ".png")
            #print("labeled image is saved to: ", savename)
            cv2.imwrite(savename, rgb) 
    
            
if __name__ == '__main__':
    
    """ below is the main() shown above 
    1. To not drain your pc memory, select samples to read by changing samplelist index.
    要避免耗尽pc内存，请通过更改样本列表索引来选择要读取的样本。
    2. This script only save component types shown at the beginning of code. 
       Change script to save other types.
       这个脚本只保存代码开头显示的组件类型。更改脚本以保存其他类型。
    """
    samplelist = [ss for ss in os.listdir(home) if ss.startswith("s") and 
                                                          not ss.endswith(".zip")]
    samplelist.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    intensities = ["20", "40", "60"]
    # mags = ["1x", "1.5x", "2x"]
    #for sample in samplelist[0:1]:
    for sample in samplelist:
        ## sample image directory
        dir_csvs = os.path.join(home, sample, "Microscope", "annotation")
        ## read sub directory for front and back side
        sides = [ss for ss in os.listdir(dir_csvs) if not ss.startswith(".")]
        #print(sides)
        """
        下面分背面和正面图片文件夹开始读取（back and front）
        """
        for side in sides:
            dir_side = os.path.join(dir_csvs, side)
            # print(dir_side)

            csvs = [ss for ss in os.listdir(dir_side) if not ss.startswith(".")]
            print("csvs now is ",csvs)
            for intensity in intensities:
                extractComponents(sample, csvs, dir_side, intensity, \
                                  savecomp=True, check=True)
 
    
    





