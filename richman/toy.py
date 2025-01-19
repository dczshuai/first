from ast import literal_eval
import random as ra
import pandas as pd
import matplotlib.pyplot as plt
import time as t
import os
import copy

def ecard(edf,cardname):#控制股票卡
    eq=input("which equity?")
    edf.at[eq,cardname]=True
    if edf.at[eq,"blackcard"] and edf.at[eq,"redcard"]:
        edf.at[eq,"blackcard"]=False
        edf.at[eq,"redcard"]=False
    return edf
