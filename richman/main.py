import random as ra
import pandas as pd
import matplotlib.pyplot as plt
import time as t
import core
import save
import extra
import toy
flag2=True#决定游戏是否继续进行
ways=0#方向
time=0#时间
width=0#地图宽度
lenth=0#地图长度
number=0#记录第几个玩家

playersaves=input("你的存档名？")
if save.check(playersaves):
    df=pd.read_excel("save/"+playersaves+"/playersave.xlsx")
else:
    while True:#初始化玩家
        x=input("多少个玩家？")
        if x.isdigit():
            x=int(x)
            break
        else:
            print("error!")
            t.sleep(1)
    playersave=core.player(x)
    df=pd.DataFrame(playersave,columns=\
    ["cash","bank","toy","way","houseplace","time","x","y","stock"])
    df.insert(0,"name","")

map=save.mapsave(playersaves)
start=core.start(df)
dicname=start[0]
dicnumber=start[1]
toyindex=start[2]
toydf=start[3]
toydic=start[4]
dics=start[5]
edf=start[6]
shoplist=start[7]
showmap=core.showmap(dicname,map)

print("S为起点，A为可购买地点，E为一圈终点")
t.sleep(1)
while flag2:#主程序
    time=core.day(df,time,number)
    pid=core.que(number,dicnumber)[0]
    number=core.que(number,dicnumber)[1]
    edf=extra.equity(edf)
    df=core.rate(df,pid)
    levelflag=flag=flag1=True
    while True and df.at[pid,"time"]==0:
        person=dicname[pid]
        x=df.at[pid,'x']
        y=df.at[pid,'y']
        print("player "+person+" time\n手头现金：",\
              df.at[pid,"cash"],"\n银行存款：",df.at[pid,"bank"])
        print("你所处位置：","("+str(x)+","+str(y)+")")
        dices=ra.randint(1,6)
        print("骰子点数为",dices)
        t.sleep(1)
        for i in showmap:
            print(i)
        t.sleep(1)
        choose=input("选择一件事去做:\ntoy\nwalk\nstock\nbuy\nshop\nrename\n")
        if choose=="toy":
            print("您拥有以下道具:")
            print(df.at[pid,"toy"])
            tid=input("选择道具名字:")
            if tid in df.at[pid,"toy"]:
                if df.at[pid,"toy"][tid]>=1:
                    df.at[pid,"toy"][tid]-=1
                    #运行toyrule函数（未编写）
                else:
                    print("error!")
                    t.sleep(1)
            else:
                print("error!")
                t.sleep(1)
        elif choose=="stock":
            df=extra.stock(df,edf,pid)
        elif choose=="walk":
            if map[y][x]!="S"\
            and map[y][x]!="E"\
            and map[y][x][1]!=-1:
                df=core.pay(df,dicname,pid)
            df=core.walk(map,df,pid,dices)
            break
        elif choose=="buy" and levelflag:
            returns=core.buy(map,df,levelflag,pid)
            map=returns[0]
            df=returns[1]
            levelflag=returns[2]
            showmap=extra.refresh(map,dicname,showmap)
        elif choose=="update" and flag and map[y][x][1]==pid:
            core.houserule(map,df,df.at[pid,"x"],df.at[pid,"y"])
            flag=False
        elif choose=="shop" and flag1:
            df=extra.shop(df,toydic,toydf,shoplist,pid)
            flag1=False
        elif choose=="stop":
            flag2=False
            df.to_excel("save/"+playersaves+"/playersave.xlsx")
            mapsave=open("save/"+playersaves+"/mapsave.txt","w")
            mapsave.write(str(map))
            mapsave.close()
            break
        elif choose=="rename":
            dicname=extra.rename(map,showmap,dicname,pid)
        else:
            print("error!")
            t.sleep(1)

df["total"]=df["cash"]+df["bank"]
for i in df.index:
    for i in df.at[i,"stock"]:
        df.at[i,"total"]+=edf[i]*df.at[i,"stock"][i]
df1=df.sort_values("total",ascending=False)
plt.title("最终排名（按照市值，不计房产）")
plt.bar(df1.name,df1.total)
plt.show()

