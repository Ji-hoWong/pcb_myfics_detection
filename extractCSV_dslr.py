#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 15:35:46 2019

@author: lvhw
"""

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
home = os.path.abspath(script_dir + "/./")

## directory for saving components 
dir_createsave = "/Saving_Extracted_Components/Subset_DSLR"
dir_save = home + dir_createsave
if os.path.exists(dir_save) == 0:
    os.makedirs(dir_save)


def extractComponents(csv, savecomp=True, check=False):
    ## get sample name "s*"
    rgb = ""
    sample = csv.split(".")[0]
    ## path of annotation file for s*
    annotation_path = os.path.join(dir_csvs, csv)
    annotation_file = pd.read_csv(annotation_path)
    print("csv file", annotation_path)
    
    ## make saving directory for components
    dir_comp_save = dir_save + "/"+ sample
    if os.path.exists(dir_comp_save) == 0:
        os.makedirs(dir_comp_save)
    
    ## read csv content
    img_names = annotation_file["image_name"]                              
    img_locations, img_attrs = readAttributes(annotation_file)
    comps_type = img_attrs["type"] 
    comps_text = img_attrs["text"]
    comps_logo = img_attrs["logo"]
        
    img_name = img_names[0]
    dir_images = os.path.join(home, sample.split("_")[0], 'DSLR', 'img')
    img, imgdir = findDSLRimg(img_name, dir_images)
    
    if check==True:
        rgb = img.copy()
    ### read each row for component attributes
    for idx in range(0, len(img_names)):  
        img_name = img_names[idx]
        
        ## read component shape for polygon, circle, rectangle
        location = img_locations[idx]
        #("location is :",type(location),location)
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
        
        ## save component or not
        if savecomp == True:
            savedir = os.path.join(dir_comp_save, comp_type)
            if os.path.exists(savedir) == 0:
                os.makedirs(savedir)
            savename = savedir + "/" + comp_type + "_" + str(idx+2) + ".png"
            cv2.imwrite(savename, img_comp)
            
    if check == True:
        savename = dir_comp_save + "/" + img_name.split(".")[0] + ".png"
        print("labeled image is saved to: ", savename)
    cv2.imwrite(savename, rgb)
    
    
if __name__ == '__main__':
    
    samplelist = [ss for ss in os.listdir(home) if ss.startswith("s") and 
                                                      not ss.endswith(".zip")]
    samplelist.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    print("samplelist is: ", samplelist)
    # for sample in samplelist[0:1]:
    for sample in samplelist:
        ## sample image directory
        print("now sample is: ", sample)
        dir_csvs = os.path.join(home, sample, "DSLR", "annotation")
        ## read csvs
        csvs = [ss for ss in os.listdir(dir_csvs) if not ss.startswith(".")]
        for csv in csvs:
            extractComponents(csv, savecomp=True, check=True)
            
    
        
        
    
    
    
    
    
    