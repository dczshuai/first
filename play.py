import random as ra
import pandas as pd
import matplotlib.pyplot as plt
import time as t

dics={"Brand":["oil","electric","airspace","house"],"per price":[200,100,150,300]}
edf=pd.DataFrame(dics,columns=["Brand","per price"],index=["oil","electric","airspace","house"])
toydic={"toyname":["controldice","blackcard","redcard","updatecard"],"per price":[1000,1000,1000,1000]}
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
while True:#初始化玩家
    x=input("多少个玩家？")
    if x.isdigit():
        x=int(x)
        break
    else:
        print("error!")
        t.sleep(1500)
while True:#初始化商店
    shoplist=input("商店里陈列多少件商品？")
    if shoplist.isdigit():
        shoplist=int(shoplist)
        break
    else:
        print("error!")
        t.sleep(1500)
def player(x):#初始化金额
    while True:
        cash=input("起始现金多少？")
        if cash.isdigit():
            cash=int(cash)
            break
        else:
            print("error!")
            t.sleep(1500)
    while True:
        bank=input("起始银行存储多少?")
        if bank.isdigit():
            bank=int(bank)
            break
        else:
            print("error!")
            t.sleep(1500)
    list1=[[cash,bank,{},ways,{},time,0,0,{}]for i in range(x)]
    return list1
playersave=player(x)
while True:
    blocks=input("地图多少格?")
    if blocks.isdigit():
        blocks=int(blocks)
        break
    else:
        print("error!")
        t.sleep(1500)
blocks=blocks-1
df=pd.DataFrame(playersave,columns=["cash","bank","toy","way","houseplace","time","x","y","stock"])
df.insert(0,"name","")
dicname={}
dicnumber={}
for i in df.index:
    df.at[i,"name"]="p"+str(i+1)
    dicnumber[df.at[i,"name"]]=i
    dicname[i]=df.at[i,"name"]

def rename(pid):
    global dicname
    rename=input("你的新名字？")
    dicname[pid]=rename
    print("你的新名字是:"+rename)

def maps(blocks):#初始化地图
    global lenth
    global width
    map=[["*"for i in range(blocks)]for i in range(blocks)]
    x=0
    y=0
    m=-1
    map[0][0]="s"
    while True:
        way=ra.randint(0,1)
        if way==0:
            x=x+1
        else:
            y=y+1
        map[y][x]=[None,None,None]
        if x+y>blocks:
            break
    while True:#去除多余地图块
        if map[-1]==["*"for i in range(blocks)]:
            map.pop()
        else:
            for j in range(-1,-len(map[-1])-1,-1):
                if map[-1][j]=="*":
                    m=j
                else:
                    break
            break
    for k in range(-1,-len(map)-1,-1):
            for l in range(-1,m,-1):
                map[k].pop()
    lenth=len(map[0])
    width=len(map)
    map[-1][-1]="e"
    return map

map=maps(blocks)



    
def dice():#骰子
    x=ra.randint(1,6)
    return x

def rate(x):#银行利率
    x=x*1.0001
    return x

def houserule(level):#房产升级规则
    if level!=None:
        if level!=6:
            while True:
                a=input("按下1升级")
                if a=="1": 
                    if df.at[pid,"cash"]>=100*level:
                        df.at[pid,"cash"]-=100*level
                        level=level+1
                        break
                    else:
                        print("error!")
                        t.sleep(1500)
                else:
                        a=input("按下1退出")
                        if a=="1":
                            break    
        else:
            print("已升至最高等级!")
    else:
        return print("error!")
    return level



def fee(pid):#基础过路费
    y=df.at[pid,"y"]
    x=df.at[pid,"x"]
    level=map[y][x][1]
    pa_ca=df.at[pid,"cash"]
    if pa_ca>=1000:
        fees=pa_ca*0.02*1.5**level
    else:
        fees=200*1.5**level
    return fees

def roadjudges(pid):#多个房子过路费
    y=df.at[pid,"y"]
    x=df.at[pid,"x"]
    owner=map[y][x][0]
    price=tmp1=tmp2=num=0
    for i in range(len(map)):
        if map[y][i][0]==owner:
            tmp1=tmp1+1
    for i in range(len(map[0])):
        if map[i][x][0]==owner:
            tmp2=tmp2+1
    num=max(tmp1,tmp2)
    price=num*fee(pid)
    return price

def pay(pid):#过路费交易
    global df
    x=df.at[pid,"x"]
    y=df.at[pid,"y"]
    df.at[map[y][x][0],"bank"]+=roadjudges(pid)
    df.at[pid,"cash"]-=roadjudges(pid)

def price(x):#基础地产价格
    prices=round(ra.uniform(1,3),2)*100
    return prices

def joke():#购买地产规则
    prices=price()
    while True:
        luck=ra.randint(1,10)
        while True:
            a=input("按1以更高的价格直接购买\n按2尝试以较低的价格购买")
            if a.isdigit():
                a=int(a)
                break
            else:
                print("error!")
                t.sleep(1500)
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
            t.sleep(1500)
        chooce=int(input("按1继续"))
        if chooce==1:
            continue
        else:
            choices=False
            return 0,choices
    choices=True
    return prices,choices

def walk(pid,dices):#玩家移动规则
    global df
    i=0
    x=df.at[pid,"x"]
    y=df.at[pid,"y"]
    while i<dices:
        if y+1<width:
            if map[y+1][x]!="*":
                y=y+1
        elif x+1<lenth:
            if map[x+1][y]!="*":
                x=x+1
        if map[y][x]=="e":
            x=0
            y=0
            df.at[pid,"cash"]+=1000
        i=i+1
    df.at[pid,"x"]=x
    df.at[pid,"y"]=y
        
def buy(pid):#金额判定
    global map
    global df
    x=df.at[pid,"x"]
    y=df.at[pid,"y"]
    if map[y][x]==[None,None,None]:
        decide=joke()
        if decide[1]:
            map[y][x][1]=pid
            if df.at[pid,"cash"]>=decide[0]:
                df.at[pid,"cash"]-=decide[0]
                return True
            else:
                print("error!")
                t.sleep(1500)
                return False
        else:
            return False

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
    for i in range(len(edf)):
        luck=ra.random()
        if luck<0.5:
            trend=False
            if luck<0.25:
                trendency=True
            else:
                trendency=False
        else:
            trend=True
            if luck>0.75:
                trendency=True
            else:
                trendency=False
        if trend:
            print(edf.at[i,"Brand"],"is upper!")
            if trendency:
                edf.at[i,"per price"]*=2
            else:
                edf.at[i,"per price"]*=1.3
        else:
            print(edf.at[i,"Brand"],"is lower!")
            if trendency:
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
    print("this is what in your hand\n",df.at[pid,"stock"])
    while True:
        choose=input("选择一个并输入:sell?buy?quit?")
        if choose=="sell":
            item=input("选择品牌："+str(edf.index))
            if item not in df.at[pid,"stock"]:
                print("error!")
                t.sleep(1500)
            else:
                while True:
                    while True:
                        num=input("数量?")
                        if num.isdigit():
                            num=int(num)
                            break
                        else:
                            print("error!")
                            t.sleep(1500)
                    if num>df.at[pid,"stock"][item]:
                        print("error!")
                        t.sleep(1500)
                    else:
                        df.at[pid,"stock"][item]-=num
                        df.at[pid,"bank"]+=edf[item,"per price"]*num
                        break
        if choose=="buy":
            item=input("选择品牌："+str(edf.index))
            if item not in edf["Brand"]:
                print("error!")
                t.sleep(1500)
            else:
                while True:
                    num=input("数量?")
                    if num.isdigit():
                        num=int(num)
                        break
                    else:
                        print("error!")
                        t.sleep(1500)
                    if df.at[pid,"bank"]<edf[item,"per price"]*num:
                        print("error!")
                        t.sleep(1500)
                    else:
                        df.at[pid,"stock"][item]+=num
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

while flag2:#主程序
    day()
    pid=que()
    person=dicname[pid]
    flag=flag1=True
    while True and df.at[pid,"time"]==0:
        print("player"+person+"time\n手头现金：",df.at[pid]["cash"],"\n银行存款：",df.at[pid]["bank"])
        print("你所处位置：",df.at[pid]['x'],df.at[pid]['y'])
        dices=dice()
        t.sleep(1500)
        for i in map:
            print(i)
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
                    t.sleep(1500)
            else:
                print("error!")
                t.sleep(1500)
        elif choose=="stock":
            stock(pid)
        elif choose=="walk":
            walk(pid,dices)
            break
        elif choose=="buy":
            buy(pid)
        elif choose=="update" and flag:
            houserule(map[df.at[pid,"y"]][df.at[pid,"x"]][1])
            flag=False
        elif choose=="shop" and flag1:
            shop(pid)
            flag1=False
        elif choose=="stop":
            flag2=False
            break
        elif choose=="rename":
            rename(pid)
        else:
            print("error!")
            t.sleep(1500)


df["total"]=df["cash"]+df["bank"]
for i in df.index:
    for i in df.at[i,"stock"]:
        df.at[i,"total"]+=edf[i]*df.at[i,"stock"][i]
df1=df.sort_values("total",ascending=False)
plt.title("最终排名（按照市值，不计房产）")
plt.bar(df1.name,df1.total)
plt.show()

