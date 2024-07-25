from ast import literal_eval
import random as ra
import pandas as pd
import matplotlib.pyplot as plt
import time as t
import os
import copy

dics={"Brand":["oil","electric","airspace","house"],"per price":[200,100,150,300]}
edf=pd.DataFrame(dics,columns=["Brand","per price"],\
                 index=["oil","electric","airspace","house"])
toydic={"toyname":["controldice","blackcard","redcard","updatecard"],\
        "per price":[1000,1000,1000,1000]}
toydf=pd.DataFrame(toydic,columns=["toyname","per price"])
toyindex={}
for i in toydf.index:
    toyindex[toydf.at[i,"toyname"]]=i
flag2=True#决定游戏是否继续进行
ways=0#方向
time=0#时间
width=0#地图宽度
lenth=0#地图长度
number=0#记录第几个玩家
        
def file_exists(directory, filename):
    file_path = os.path.join(directory, filename)# 构建完整的文件路径
    if os.path.exists(file_path):# 检查文件是否存在
        return True
    else:
        return False

playersaves=input("你的存档名？")
def maps(blocks):#初始化地图
    global lenth
    global width
    map=[[[None,None,None]for i in range(blocks)]for i in range(blocks)]
    x=0
    y=0
    m=-1
    map[0][0]="S"
    while True:
        way=ra.randint(0,1)
        if way==0:
            x=x+1
        else:
            y=y+1
        map[y][x]=[0,-1,-1]
        if x+y>=blocks-1:
            break
    while True:#去除多余地图块
        if map[-1]==[[None,None,None]for i in range(blocks)]:
            map.pop()
        else:
            for j in range(-1,-len(map[-1])-1,-1):
                if map[-1][j]==[None,None,None]:
                    m=j
                else:
                    break
            break
    for k in range(-1,-len(map)-1,-1):
            for l in range(-1,m,-1):
                map[k].pop()
    lenth=len(map[0])
    width=len(map)
    map[-1][-1]="E"
    return map

def player(x):#初始化金额
    while True:
        cash=input("起始现金多少？")
        if cash.isdigit():
            cash=float(cash)
            break
        else:
            print("error!")
            t.sleep(1)
    while True:
        bank=input("起始银行存储多少?")
        if bank.isdigit():
            bank=float(bank)
            break
        else:
            print("error!")
            t.sleep(1)
    list1=[[cash,bank,{},ways,{},time,0,0,{}]for i in range(x)]
    return list1
if not file_exists("","save"):#检测是否有存档
    os.mkdir("save")
if not file_exists("save",playersaves):#检测是否有存档
    os.mkdir("save/"+playersaves)
if file_exists("save/"+playersaves,"playersave.xlsx"):
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
    playersave=player(x)
    df=pd.DataFrame(playersave,columns=\
    ["cash","bank","toy","way","houseplace","time","x","y","stock"])
    df.insert(0,"name","")
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
    map=maps(blocks)

while True:#初始化商店
    shoplist=input("商店里陈列多少件商品？")
    if shoplist.isdigit():
        shoplist=int(shoplist)
        break
    else:
        print("error!")
        t.sleep(1)



dicname={}
dicnumber={}
for i in df.index:
    df.at[i,"name"]="p"+str(i+1)
    dicnumber[df.at[i,"name"]]=i
    dicname[i]=df.at[i,"name"]

showmap=copy.deepcopy(map)
# showmap=[]
# for maptmp in map:
#     showmap.append(maptmp)

for line in showmap:
    for line in range(len(showmap)):
        for element in range(len(showmap[line])):
            if map[line][element]!="S"\
            and map[line][element]!="E":
                if map[line][element][1] in dicname:
                    showmap[line][element][0]=\
                    dicname[map[line][element][1]]\
                    +str(map[line][element][0])
                elif showmap[line][element]==[None,None,None]:
                    showmap[line][element]="*"
                elif showmap[line][element]==[0,-1,-1]:
                    showmap[line][element]="A"

def refresh():
    global showmap
    for line in range(len(map)):
        for element in range(len(map[line])):
            if map[line][element]!="S" and map[line][element]!="E":
                if map[line][element][1] in dicname:
                    change=dicname[map[line][element][1]]\
                    +str(map[line][element][0])
                    showmap[line][element]=change

def rename(pid):
    global dicname
    global showmap
    rename=input("你的新名字？")
    dicname[pid]=rename
    refresh()
    print("你的新名字是:"+rename)

def rate(x):#银行利率
    x=x*1.0001
    return x

def houserule(x,y,pid):#房产升级规则
    global map
    global levelflag
    if map[y][x][1]!=6:
        while True:
            a=input("按下1升级")
            if a=="1": 
                if df.at[pid,"cash"]>=100*map[y][x][0]:
                    df.at[pid,"cash"]-=100*map[y][x][0]
                    map[y][x][0]=map[y][x][0]+1
                    levelflag=False
                    break
                else:
                    print("error!")
                    t.sleep(1)
            else:
                    a=input("按下1退出")
                    if a=="1":
                        break    
    else:
        print("已升至最高等级!")

def fee(pid):#基础过路费
    y=df.at[pid,"y"]
    x=df.at[pid,"x"]
    level=map[y][x][0]
    pa_ca=df.at[pid,"cash"]
    if pa_ca>=1000:
        fees=pa_ca*0.02*1.5**level
    else:
        fees=200*1.5**level
    return fees

def roadjudges(pid):#多个房子过路费
    y=df.at[pid,"y"]
    x=df.at[pid,"x"]
    owner=map[y][x][1]
    price=tmp1=tmp2=num=0
    for i in range(len(map)):
        if map[y][i][1]==owner:
            tmp1=tmp1+1
    for i in range(len(map[0])):
        if map[i][x][1]==owner:
            tmp2=tmp2+1
    num=max(tmp1,tmp2)
    price=num*fee(pid)
    return price

def pay(pid):#过路费交易
    global df
    x=df.at[pid,"x"]
    y=df.at[pid,"y"]
    df.at[map[y][x][1],"bank"]+=roadjudges(pid)
    df.at[pid,"cash"]-=roadjudges(pid)

def price():#基础地产价格
    prices=round(ra.uniform(1,3),2)*100
    return prices

def joke():#购买地产规则
    prices=price()
    while True:
        print("当前价格为",prices)
        luck=ra.randint(1,10)
        while True:
            a=input("按1以1.5倍价格直接购买\n按2尝试以较低的价格购买")
            if a.isdigit():
                a=int(a)
                break
            else:
                print("error!")
                t.sleep(1)
        if a==2:
            if luck<=5:
                prices=prices*1.5
            else:
                break
        elif a==1:
            prices=prices*1.5
            break
        else:
            print("error!")
            t.sleep(1)
        chooce=input("按1继续")
        if chooce=="1":
            continue
        else:
            choices=False
            return -1,choices
    choices=True
    print("购买成功！")
    t.sleep(1)
    return prices,choices

def walk(pid,dices):#玩家移动规则
    global df
    i=0
    x=df.at[pid,"x"]
    y=df.at[pid,"y"]
    while i<dices:
        if map[y][x]=="E":
            x=0
            y=0
            df.at[pid,"cash"]+=1000
            print("你走完了一圈！")
        elif y+1<width:
            if map[y+1][x]!=[None,None,None]:
                y=y+1
            elif x+1<lenth:
                if map[y][x+1]!=[None,None,None]:
                    x=x+1
        i=i+1
    df.at[pid,"x"]=x
    df.at[pid,"y"]=y
        
def buy(pid):#金额判定
    global map
    global df
    global levelflag
    x=df.at[pid,"x"]
    y=df.at[pid,"y"]
    if map[y][x]==[0,-1,-1]:
        decide=joke()
        if decide[1]:
            map[y][x][1]=pid
            if df.at[pid,"cash"]>=decide[0]:
                df.at[pid,"cash"]-=decide[0]
                levelflag=False
                return True
            else:
                print("金钱不够!")
                t.sleep(1)
                return False
        else:
            return False
    elif map[y][x]!="S"\
    and map[y][x]!="E":
        if map[y][x][1]==pid:
            houserule(x,y,pid)
    else:
        print("error!")

def que():#玩家队列
    global number
    ids=0
    while True:
        if number<len(dicnumber):
            ids=number
            number=number+1
            return ids
        else:
            number=0

def equity():#股市规则
    global edf
    for i in edf.index:
        luck=ra.random()
        if luck<0.5:
            trend=False
            if luck<0.2:
                trendency=True
            else:
                trendency=False
        else:
            trend=True
            if luck>0.7:
                trendency=True
            else:
                trendency=False
        if trend:
            print(i,"涨了!")
            if trendency:
                print(i,"大涨！涨疯了!")
                edf.at[i,"per price"]*=2
            else:
                edf.at[i,"per price"]*=1.3
        else:
            print(i,"跌了!")
            if trendency:
                print(i,"大跌！跳楼了！")
                edf.at[i,"per price"]/=3
            else:
                edf.at[i,"per price"]/=1.5
        round(edf.at[i,"per price"])
    print("今日价格:\n",edf)

def day():#时间规则
    global df
    global time
    if number==0:
        for i in df.index:
            if df.at[i,"time"]!=0:
                df.at[i,"time"]-=1
        time+=1
        print("今天是第",time,"天")
    
def ecard(cardname):#控制股票卡
    eq=input("which equity?")
    edf.at[eq,cardname]=True
    if edf.at[eq,"blackcard"] and edf.at[eq,"redcard"]:
        edf.at[eq,"blackcard"]=False
        edf.at[eq,"redcard"]=False
        
def stock(pid):#股票
    global df
    print("你手中有这些\n",df.at[pid,"stock"])
    while True:
        choose=input("选择一个并输入:出售输入sell，购买输入buy?退出输入quit?")
        if choose=="sell":
            item=input("选择品牌："+str(edf.index))
            if item not in df.at[pid,"stock"]:
                print("error!")
                t.sleep(1)
            else:
                while True:
                    while True:
                        num=input("数量?")
                        if num.isdigit():
                            num=int(num)
                            break
                        else:
                            print("error!")
                            t.sleep(1)
                    if num>df.at[pid,"stock"][item]:
                        print("error!")
                        t.sleep(1)
                    else:
                        df.at[pid,"stock"][item]-=num
                        df.at[pid,"bank"]+=edf[item,"per price"]*num
                        break
        if choose=="buy":
            item=input("选择品牌："+str(edf.index))
            if item not in edf["Brand"]:
                print("error!")
                t.sleep(1)
            else:
                while True:
                    num=input("数量?")
                    if num.isdigit():
                        num=int(num)
                        break
                    else:
                        print("error!")
                        t.sleep(1)
                    if df.at[pid,"bank"]<edf[item,"per price"]*num:
                        print("error!")
                        t.sleep(1)
                    else:
                        if item in df.at[pid,"stock"]:
                            df.at[pid,"stock"][item]+=num
                        else:
                            df.at[pid,"stock"][item]=num
                        df.at[pid,"bank"]-=edf[item,"per price"]*num
                        break
        if choose=="quit":
            break

def shop(pid):#超市
    item={}
    while True:
        num=ra.randint(1,len(toydic)-1)
        if toydic[num] not in item:
            item[toydf.at[num,"toyname"]]=toydf.at[num,"per price"]
            if len(item)>=shoplist:
                break
    print(item)
    while True:
        buy=input("输入你要购买的商品名称或者输入quit退出")
        if buy in item and item[buy]<df.at[pid,"cash"]:
            df.at[pid,"cash"]-=item[buy]
        if buy in df.at[pid,"toy"]:
            df.at[pid,"toy"][buy]+=1
        else:
            df.at[pid,"toy"][buy]=1
            item.pop[buy]

print("S为起点，A为可购买地点，E为一圈终点")
t.sleep(1)
while flag2:#主程序
    day()
    pid=que()
    equity()
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
            stock(pid)
        elif choose=="walk":
            walk(pid,dices)
            if map[y][x]!="S"\
            and map[y][x]!="E"\
            and map[y][x][1]!=-1:
                pay(pid)
            break
        elif choose=="buy" and levelflag:
            buy(pid)
            refresh()
        elif choose=="update" and flag:
            houserule(map[df.at[pid,"y"]][df.at[pid,"x"]][1])
            flag=False
        elif choose=="shop" and flag1:
            shop(pid)
            flag1=False
        elif choose=="stop":
            flag2=False
            df.to_excel("save/"+playersaves+"/playersave.xlsx")
            mapsave=open("save/"+playersaves+"/mapsave.txt","w")
            mapsave.write(str(map))
            mapsave.close()
            break
        elif choose=="rename":
            rename(pid)
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

