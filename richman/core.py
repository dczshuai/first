import random as ra
import pandas as pd
import time as t
import copy
import extra

def start(df):
    dics={"Brand":["oil","electric","airspace","house"],"per price":[200,100,150,300]}
    edf=pd.DataFrame(dics,columns=["Brand","per price"],\
                    index=["oil","electric","airspace","house"])
    toydic={"toyname":["controldice","blackcard","redcard","updatecard"],\
            "per price":[1000,1000,1000,1000]}
    toydf=pd.DataFrame(toydic,columns=["toyname","per price"])
    toyindex={}
    for i in toydf.index:
        toyindex[toydf.at[i,"toyname"]]=i
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
    return dicname,dicnumber,toyindex,toydf,toydic,dics,edf,shoplist

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
    list1=[[cash,bank,{},0,{},0,0,0,{}]for i in range(x)]
    return list1

def showmap(dicname,map):
    showmap=copy.deepcopy(map)
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
                        showmap[line][element]=" "
                    elif showmap[line][element]==[0,-1,-1]:
                        showmap[line][element]="A"
    return showmap


def rate(df,pid):#银行利率
    df.at[pid,"bank"]*=1.001
    return df

def houserule(map,df,x,y,pid):#房产升级规则
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
    return map

def fee(df,pid):#基础过路费
    y=df.at[pid,"y"]
    x=df.at[pid,"x"]
    level=map[y][x][0]
    pa_ca=df.at[pid,"cash"]
    if pa_ca>=1000:
        fees=pa_ca*0.02*1.5**level
    else:
        fees=200*1.5**level
    return fees

def roadjudges(df,pid):#多个房子过路费
    y=df.at[pid,"y"]
    x=df.at[pid,"x"]
    owner=map[y][x][1]
    price=tmp1=tmp2=num=0
    if owner==pid:
        return 0
    else:
        for i in range(lenth):
            if map[y][i]!="S"\
            and map[y][i]!="E":
                if map[y][i][1]==owner:
                    tmp1=tmp1+1
        for i in range(width):
            if map[i][x]!="S"\
            and map[i][x]!="E":
                if map[i][x][1]==owner:
                    tmp2=tmp2+1
        num=max(tmp1,tmp2)
        price=num*fee(pid)
    return price

def pay(df,dicname,pid):#过路费交易
    x=df.at[pid,"x"]
    y=df.at[pid,"y"]
    passfee=roadjudges(df,pid)
    owner=map[y][x][1]
    df.at[pid,"cash"]-=passfee
    print(dicname[pid],"缴纳现金过路费:",passfee)
    df.at[map[y][x][1],"bank"]+=passfee
    print(dicname[owner],"银行到账过路费:",passfee)
    return df

def price():#基础地产价格
    prices=round(ra.uniform(1,3),2)*100
    return prices



def walk(map,df,pid,dices):#玩家移动规则
    i=0
    x=df.at[pid,"x"]
    y=df.at[pid,"y"]
    while i<dices:
        if map[y][x]=="E":
            x=0
            y=0
            df.at[pid,"cash"]+=1000
            print("手头现金：",\
              df.at[pid,"cash"],"\n"\
                "银行存款：",df.at[pid,"bank"])
            print("你走完了一圈！")
            extra.bank(df,pid)
        else:
            if y+1==width:
                x=x+1
            elif map[y+1][x]!=[None,None,None]:
                y=y+1
            else:
                x=x+1
        i=i+1
    df.at[pid,"x"]=x
    df.at[pid,"y"]=y
    return df

def buy(map,df,levelflag,pid):#金额判定
    x=df.at[pid,"x"]
    y=df.at[pid,"y"]
    if map[y][x]==[0,-1,-1]:
        decide=extra.joke()
        if decide[1]:
            map[y][x][1]=pid
            if df.at[pid,"cash"]>=decide[0]:
                df.at[pid,"cash"]-=decide[0]
                levelflag=False
                return map,df,levelflag
            else:
                print("金钱不够!")
                t.sleep(1)
                return map,df,levelflag
        else:
            print("error!")
            return map,df,levelflag
    else:
        print("error!")
        return map,df,levelflag

def que(number,dicnumber):#玩家队列
    ids=0
    while True:
        if number<len(dicnumber):
            ids=number
            number=number+1
            return ids,number
        else:
            number=0
            return 0,number

def day(df,time,number):#时间规则
    if number==0:
        for i in df.index:
            if df.at[i,"time"]!=0:
                df.at[i,"time"]-=1
        time+=1
        print("今天是第",time,"天")
    return time



