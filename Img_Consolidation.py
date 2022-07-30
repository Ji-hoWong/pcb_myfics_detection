# coding=utf-8
import shutil
from utils import *
from os.path import dirname, abspath



script_dir = dirname(dirname(abspath(__file__)))
home = os.path.abspath(script_dir + "/./")

## directory for saving components
dir_createsave = "\\Saving_Extracted_Images"
dir_save = home + dir_createsave
subpath = "./"
if __name__ == '__main__':
    determination = dir_save
    if not os.path.exists(determination):
        os.makedirs(determination)
    """
    samplelist = [ss for ss in os.listdir(home) if ss.startswith("s") and
                  not ss.endswith(".zip") and ss != "s13"]
    samplelist.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    #print("samplelist is: ", samplelist)
    # for sample in samplelist[0:1]:
    for sample in samplelist:
        ## sample image directory
        #print("now sample is: ", sample)
        dir_imgs = os.path.join(home, sample, "DSLR", "img")
        ## read csvs
        imgs = [ss for ss in os.listdir(dir_imgs) if not ss.startswith(".")]
        print("now imgs is :", imgs)
        for img in imgs:
            shutil.copyfile(dir_imgs+ "\\" + img, dir_save + '/' + str(img))
    """
    samplelist = [ss for ss in os.listdir(home) if ss.startswith("s") and
                  not ss.endswith(".zip")]
    samplelist.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    intensities = ["20", "40", "60"]
    # mags = ["1x", "1.5x", "2x"]
    # for sample in samplelist[0:1]:
    for sample in samplelist:
        ## sample image directory
        dir_csvs = os.path.join(home, sample, "Microscope", "annotation")
        ## read sub directory for front and back side
        sides = [ss for ss in os.listdir(dir_csvs) if not ss.startswith(".")]
        # print(sides)
        """
        下面分背面和正面图片文件夹开始读取（back and front）
        """
        for side in sides:
            dir_side = os.path.join(dir_csvs, side)
            print(dir_side)

            csvs = [ss for ss in os.listdir(dir_side) if not ss.startswith(".")]
            print("csvs now is ", csvs)
            for csv in csvs:
                print("csv now is ", csv)
                annotation_path = os.path.join(dir_side, csv)
                annotation_file = pd.read_csv(annotation_path)

                img_names = annotation_file["image_name"]
                #print("img_names is",img_names)
                if len(img_names):
                    prev_name = img_names[0]
                    for idx in range(0, len(img_names)):
                        #print("img_name is:", img_names[idx])
                        img_name = img_names[idx]
                        # 如果读取第一个，或者与上一个图片不同
                        if idx == 0 or img_name != prev_name:
                            mag = img_name.split("_")[2]
                            #print("mag is:", mag)
                            dir_sub = ("_").join(img_name.split("_")[0:5])
                            #print("img_name is:", img_name, "\ndir_sub is:", dir_sub)
                            foldername = os.path.join(home, sample, "Microscope", "img", side)
                            dir_img = os.path.join(foldername, mag, dir_sub, "TileScan_001", img_name)
                            print("dir_img is:", dir_img)
                            shutil.copyfile(dir_img, dir_save + '/' + str(img_name))
                            prev_name = img_name
