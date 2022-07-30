from utils import *
from os.path import dirname, abspath

if __name__ == '__main__':
    script_dir = dirname(dirname(abspath(__file__)))
    print(script_dir)
    home = os.path.abspath(script_dir + "/./")
    print(home)
    idx = 1
    samplelist = [ss for ss in os.listdir(home) if ss.startswith("s") and
                                                          not ss.endswith(".zip") and ss != "s13"]
    samplelist.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    print("samplelist is: ", samplelist)
    # for sample in samplelist[0:1]:
    for sample in samplelist:
        ## sample image directory
        print("now sample is: ", sample)
        dir_csvs = os.path.join(home, sample, "DSLR", "annotation")
        ## read csvs
        csvs = [ss for ss in os.listdir(dir_csvs) if not ss.startswith(".")]
        print("now csvs is :",csvs)
        for csv in csvs:
            annotation_path = os.path.join(dir_csvs, csv)
            df = pd.read_csv(annotation_path)
            if idx == 1:
                df.to_csv('all2022.csv', mode='a', index=False)
                idx = 0
            else:
                df.to_csv('all2022.csv', mode='a', index=False, header=False)

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
            # print(dir_side)

            csvs = [ss for ss in os.listdir(dir_side) if not ss.startswith(".")]

            for csv in csvs:
                annotation_path = os.path.join(dir_side, csv)
                df = pd.read_csv(annotation_path)
                df.to_csv('all2022.csv', mode='a', index=False, header=None)