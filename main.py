from captcha_gen import Captcha
import image_process, image_training, image_feature
from config import captcha_path, train_data_path, test_data_path, train_data_tmp_path
import os, shutil, pathlib

def link_files():
    all_c = os.listdir(captcha_path)
    test_c = all_c[-60:]
    trp = pathlib.Path(train_data_path)
    if not trp.exists(): trp.mkdir()
    tsp = pathlib.Path(test_data_path)
    if not tsp.exists(): tsp.mkdir()
    cpr = captcha_path[captcha_path.rindex('/'):]
    trr = train_data_path[train_data_path.rindex('/'):]
    trtmp = pathlib.Path(train_data_path + "/tmp")
    if not trtmp.exists(): trtmp.mkdir()
    with open("link.sh", "wb") as s:
        s.write("#!/bin/bash\n".encode("utf-8"))
        s.write(("cd "+os.getcwd()+"/"+train_data_path+" && find .."+cpr+" -name \"*.png\" | xargs -I {} ln -s ../{} ./tmp\n").encode("utf-8"))
        s.write(("cd "+os.getcwd()+"/"+test_data_path+"\n").encode("utf-8"))
        for f in test_c:
            s.write(("ln -s .."+cpr+"/"+f+" ./\n").encode("utf-8"))
            s.write(("rm -f .."+trr+"/tmp/"+f+"\n").encode("utf-8"))
        os.system("bash link.sh")

if __name__ == '__main__':
    Captcha(660, captcha_path, "白舟忍者", 48).gen_captcha()
    link_files()
    image_process.main()
    os.system("rm -rf "+train_data_tmp_path)
    image_feature.main()
    image_training.main()