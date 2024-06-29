import random as ra
import pandas as pd
import matplotlib.pyplot as plt

dics={"Brand":["oil","electric","airspace","house"],"per price":[200,100,150,300]}
edf=pd.DataFrame(dics,columns=["Brand","per price"],index=["oil","electric","airspace","house"])
toydic={"toyname":["controldice","blackcard","redcard","updatecard"],"per price":[1000,1000,1000,1000]}
toydf=pd.DataFrame(toydic,columns=["toyname","per price"])
toyindex={}
for i in toydf.index:
    toyindex[toydf.at[i,"toyname"]]=i
ways=0
time=0
width=0
lenth=0
number=0
flag2=True
while True:
    x=input("how many players?")
    if x.isdigit():
        x=int(x)
        break
    else:
        print("error!")
while True:
    shoplist=input("how many list in shop?")
    if shoplist.isdigit():
        shoplist=int(shoplist)
        break
    else:
        print("error!")
def player(x):
    while True:
        money=input("how much start?")
        if money.isdigit():
            money=int(money)
            break
        else:
            print("error!")
    while True:
        bank=input("how much in bank?")
        if bank.isdigit():
            bank=int(bank)
            break
        else:
            print("error!")
    list1=[[money,bank,{},ways,{},time,0,0,{}]for i in range(x)]
    return list1
a=player(x)
while True:
    b=input("how many blocks?")
    if b.isdigit():
        b=int(b)
        break
    else:
        print("error!")
b=b-1
df=pd.DataFrame(a,columns=["money","bank","toy","way","houseplace","time","x","y","stock"])
df.insert(0,"name","")
dicname={}
dicnumber={}
for i in df.index:
    df.at[i,"name"]="p"+str(i+1)
    dicnumber[df.at[i,"name"]]=i
    dicname[i]=df.at[i,"name"]
def maps(b):
    global lenth
    global width
    st=[["*"for i in range(b)]for i in range(b)]
    x=0
    y=0
    st[0][0]="s"
    while True:
        way=ra.randint(0,1)
        if way==0:
            x=x+1
        else:
            y=y+1
        st[y][x]=[None,None,None]
        if x+y>b:
            break
    while True:
        if st[-1]==["*"for i in range(b)]:
            st.pop()
        else:
            for j in range(-1,-len(st[-1])-1,-1):
                if st[-1][j]=="*":
                    m=j
                else:
                    m=-1
                    break
            break
    for k in range(-1,-len(st)-1,-1):
            for l in range(-1,m,-1):
                st[k].pop()
    lenth=len(st[0])
    width=len(st)
    st[-1][-1]="e"
    return st

st=maps(b)
#初始化地图玩家


# def shop():
#     
    
def dice():
    x=ra.randint(1,6)
    return x

def rate(x):
    x=x*1.0001
    return x

def houserule(x):
    if x!=None:
        if x!=6:
            while True:
                a=input("press 1 to up level")
                if a=="1": 
                    if df.at[pid,"cash"]>=100*x:
                        df.at[pid,"cash"]-=100*x
                        x=x+1
                        break
                    else:
                        print("error!")
                else:
                        a=input("press 1 to quit")
                        if a=="1":
                            break    
        else:
            print("it is up to maximum!")
    else:
        return print("error!")
    return x



def fee(pid):
    y=df.at[pid,"y"]
    x=df.at[pid,"x"]
    level=st[y][x][1]
    pa_ca=df.at[pid,"cash"]
    if pa_ca>=1000:
        fees=pa_ca*0.02*1.5**level
    else:
        fees=200*1.5**level
    return fees

def roadjudges(pid):
    y=df.at[pid,"y"]
    x=df.at[pid,"x"]
    owner=st[y][x][0]
    price=tmp1=tmp2=num=0
    for i in range(len(st)):
        if st[y][i][0]==owner:
            tmp1=tmp1+1
    for i in range(len(st[0])):
        if st[i][x][0]==owner:
            tmp2=tmp2+1
    num=max(tmp1,tmp2)
    price=num*fee(pid)
    return price

def pay(pid):
    global df
    x=df.at[pid,"x"]
    y=df.at[pid,"y"]
    df.at[st[y][x][0],"bank"]+=roadjudges(pid)
    df.at[pid,"cash"]-=roadjudges(pid)

def price(x):
    prices=round(ra.uniform(1,3),2)*100
    return prices

def joke():
    prices=price()
    while True:
        luck=ra.randint(1,10)
        while True:
            a=input("print 1 to buy it in high price/nprint 2 to try to buy it in low price")
            if a.isdigit():
                a=int(a)
                break
            else:
                print("error!")
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
        chooce=int(input("if continue,press'1'"))
        if chooce==1:
            continue
        else:
            choices=False
            return 0,choices
    choices=True
    return prices,choices

def walk(pid,dices):
    global df
    i=0
    x=df.at[pid,"x"]
    y=df.at[pid,"y"]
    while i<dices:
        if y+1<width:
            if st[y+1][x]!="*":
                y=y+1
        elif x+1<lenth:
            if st[x+1][y]!="*":
                x=x+1
        if st[y][x]=="e":
            x=0
            y=0
            df.at[pid,"cash"]+=1000
        i=i+1
    df.at[pid,"x"]=x
    df.at[pid,"y"]=y
        
def buy(pid):
    global st
    global df
    x=df.at[pid,"x"]
    y=df.at[pid,"y"]
    if st[y][x]==[None,None,None]:
        decide=joke()
        if decide[1]:
            st[y][x][1]=pid
            if df.at[pid,"cash"]>=decide[0]:
                df.at[pid,"cash"]-=decide[0]
                return True
            else:
                print("error!")
                return False
        else:
            return False

def que():
    global number
    ids=0
    while True:
        if number<len(dicnumber):
            ids=number
            number=number+1
            return ids
        else:
            number=0

def equity():
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
    print("today price:/n",edf)

def day():#回合跳过累计
    global df
    global time
    if number==0:
        for i in df.index:
            if df.at[i,"time"]!=0:
                df.at[i,"time"]-=1
        time+=1
        print("today is ",time,"time")
    
def ecard(cardname):#控制股票卡
    eq=input("which equity?")
    edf.at[eq,cardname]=True
    if edf.at[eq,"blackcard"] and edf.at[eq,"redcard"]:
        edf.at[eq,"blackcard"]=False
        edf.at[eq,"redcard"]=False
        
def stock(pid):#股票
    global df
    print("this is what in your hand/n",df.at[pid,"stock"])
    while True:
        choose=input("choose one:sell?buy?quit?")
        if choose=="sell":
            item=input("brand?")
            if item not in df.at[pid,"stock"]:
                print("error!")
            else:
                while True:
                    
                    while True:
                        num=input("amount?")
                        if num.isdigit():
                            num=int(num)
                            break
                        else:
                            print("error!")
                    if num>df.at[pid,"stock"][item]:
                        print("error!")
                    else:
                        df.at[pid,"stock"][item]-=num
                        df.at[pid,"bank"]+=edf[item,"per price"]*num
                        break
        if choose=="buy":
            item=input("brand?")
            if item not in edf["Brand"]:
                print("error!")
            else:
                while True:
                    num=input("amount?")
                    if num.isdigit():
                        num=int(num)
                        break
                    else:
                        print("error!")
                    if df.at[pid,"bank"]<edf[item,"per price"]*num:
                        print("error!")
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
        buy=input("what you want? or input quit to quit")
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
    person=dicname(pid)
    flag=flag1=True
    while True and df.at[pid,"time"]!=0:
        print("player"+person+"time")
        dices=dice()
        choose=input("choose one to do:\ntoy\nwalk\nstock\nbuy\nshop")
        if choose=="toy":
            print("the toys you can choose are below:")
            print(df.at[pid,"toy"])
            tid=input("input the toy name:")
            if df.at[pid,"toy"][tid]>=1:
                df.at[pid,"toy"][tid]-=1
                #运行toyrule函数（未编写）
            else:
                print("error!")
        elif choose=="stock":
            stock(pid)
        elif choose=="walk":
            walk(pid,dices)
            break
        elif choose=="buy":
            buy(pid)
        elif choose=="update" and flag:
            houserule(st[df.at[pid,"y"]][df.at[pid,"x"]][1])
            flag=False
        elif choose=="shop" and flag1:
            shop(pid)
            flag1=False
        elif choose=="stop":
            break
        else:
            print("error!")
        for i in st:
            print(i)

df["total"]=df["cash"]+df["bank"]
for i in df.index:
    for i in df.at[i,"stock"]:
        df.at[i,"total"]+=edf[i]*df.at[i,"stock"][i]
df1=df.sort_values("total",ascending=False)
plt.title("最终排名（按照市值，不计房产）")
plt.bar(df1.name,df1.total)
plt.show()

