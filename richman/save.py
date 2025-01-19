from ast import literal_eval
import pandas as pd
import time as t
import os
import core

def file_exists(directory, filename):
    file_path = os.path.join(directory, filename)# 构建完整的文件路径
    if os.path.exists(file_path):# 检查文件是否存在
        return True
    else:
        return False

def check(playersaves):
    if not file_exists("","save"):#检测是否有存档
        os.mkdir("save")
    if not file_exists("save",playersaves):#检测是否有存档
        os.mkdir("save/"+playersaves)
    if file_exists("save/"+playersaves,"playersave.xlsx"):
        df=pd.read_excel("save/"+playersaves+"/playersave.xlsx")
        return True
    else:
        return False

def mapsave(playersaves):
    if file_exists("save/"+playersaves,"mapsave.txt"):
        mapsave=open("save/"+playersaves+"/mapsave.txt","r")
        map=literal_eval(mapsave.read())
        mapsave.close()
    else:
        while True:#设置地图格数
            blocks=input("地图多少格?要求大于3\n")
            if blocks.isdigit():
                blocks=int(blocks)
                if blocks>3:
                    break
            else:
                print("error!")
                t.sleep(1)
        map=core.maps(blocks)
    return map