import random as ra
import pandas as pd

ways=0

time=0

def player(x):
    money=int(input("how much start?"))
    bank=int(input("how much in bank?"))
    list1=[[money,bank,{},ways,{},time]for i in range(x)]
    return list1


# def shop():
#     
    
def dice():
    x=ra.randint(1,6)
    return x

def rate(x):
    x=x*1.0001
    return x

def houserule(x):
    like=True
    if x!=6:
        while like:
            a=int(input("press 1 to up level"))
            if a==1:
                x=x+1
                break
            else:
                a=int(input("press 1 to sure"))
                if a==1:
                    break
    else:
        print("it is up to maximum!")
    return x

def maps(a):
    global lenth
    global width
    st=[["*"for i in range(a)]for i in range(a)]
    x=0
    y=0
    st[0][0]="s"
    while True:
        way=ra.randint(0,1)
        if way==0:
            x=x+1
        else:
            y=y+1
        st[x][y]=[]
        if x+y>=a-1:
            break
    while True:
        if st[-1]==["*"for i in range(a)]:
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
        if m==-1:
            break
        else:
            for l in range(-1,m-1,-1):
                st[k].pop()
    lenth=len(st[0])
    width=len(st)
    st[-1][-1]="e"
    return st


def fee(x,y,name):
    level=st[x][y][1]
    df.at[name,"cash"]=pa_ca
    if pa_ca>=1000:
        fees=pa_ca*0.02*1.5**level
    return fees

def judge(x,y,name):
    owner=st[x][y]
    price=tmp1=tmp2=num=0
    for i in range(len(st)):
        if st[i][y][0]==owner:
            tmp1=tmp1+1
    for i in range(len(st[0])):
        if st[x][i][0]==owner:
            tmp2=tmp2+1
    num=max(tmp1,tmp2)
    price=num*fee(x,y,name)
    return price

def pay(x,y,name):
    df.at[st[x][y][0],"bank"]+=judge(x,y,name)
    df.at[name,"cash"]-=judge(x,y,name)

def price(x):
    prices=round(ra.uniform(1,3),2)*100
    return prices

def jock(x,name):
    prices=price()
    while True:
        luck=ra.randint(1,10)
        a=int(input("print 1 to buy it in high price/nprint 2 to try to buy it in low price"))
        if a==2:
            if luck<=5:
                prices=prices*1.5
            else:
                break
        elif a==1:
            prices=prices*1.5
            break
        chooce=int(input("if continue,press'1'"))
        if chooce==1:
            continue
        else:
            choices=False
            return 0,choices
    choices=True
    return prices,choices

# def walk(name):
#     dices=dice()
#     while dices>0:
        

        
    
choice=True


x=int(input("how many players?"))
a=player(x)
b=int(input("how many blocks?"))
df=pd.DataFrame(a,columns=["money","bank","toy","way","houseplace","time"])
df.insert(0,"name","")
dic={}
for i in df.index:
    df.at[i,"name"]="p"+str(i+1)
    dic[df.at[i,"name"]]=i

# while choice:
#     for i in df.index:
#         print("player"+str(i+1)+"time")
#         a=" "
#         while a!="":
#             a=input("choose one to do:\n1:shop\n2:toy\n")
#             if a=="1":
print(dic)
