import random as ra
import time as t
import core

def refresh(map,dicname,showmap):
    for line in range(len(map)):
        for element in range(len(map[line])):
            if map[line][element]!="S" and map[line][element]!="E":
                if map[line][element][1] in dicname:
                    change=dicname[map[line][element][1]]\
                    +str(map[line][element][0])
                    showmap[line][element]=change
    return showmap

def rename(map,showmap,dicname,pid):
    rename=input("你的新名字？")
    dicname[pid]=rename
    refresh(map,dicname,showmap)
    print("你的新名字是:"+rename)
    return dicname

def bank(df,pid):
    while True:
        choose=input("取款输入1，存款输入2")
        if choose=="1" or choose=="2":
            choose=int(choose)
            break
        else:
            print("error!")
            t.sleep(1)
    while True:
        withdraw=input("你要取/存多少钱?")
        if withdraw.isdigit():
            withdraw=float(withdraw)
            if df.at[pid,"bank"]>=withdraw and choose==1:
                df.at[pid,"bank"]-=withdraw
                df.at[pid,"cash"]+=withdraw
                break
            elif df.at[pid,"cash"]>=withdraw and choose==2:
                df.at[pid,"cash"]-=withdraw
                df.at[pid,"bank"]+=withdraw
                break
            else:
                print("error!")
                t.sleep(1)
        else:
            print("error!")
            t.sleep(1)
    return df

def joke():#购买地产规则
    prices=core.price()
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

def equity(edf):#股市规则
    for i in edf.index:
        luck=ra.random()
        business=ra.random()
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
                edf.at[i,"per price"]*=ra.randint(5,10)
            else:
                edf.at[i,"per price"]*=ra.randint(2,4)
        else:
            print(i,"跌了!")
            if trendency:
                print(i,"大跌！跳楼了！")
                edf.at[i,"per price"]*=ra.uniform(0.1,0.3)
            else:
                edf.at[i,"per price"]*=ra.uniform(0.5,0.9)
        if business>0.69 or business<0.39:
            storm=ra.randint(0,len(edf)-1)
            print("大商有所动作！")
            if business>0.69:
                edf[storm]
        round(edf.at[i,"per price"])
    print("今日价格:\n",edf)
    return edf

def stock(df,edf,pid):#股票
    print("你手中有这些\n",df.at[pid,"stock"])
    while True:
        choose=input("选择一个并输入:出售输入sell，购买输入buy?退出输入quit?\n\
tip:只能用银行存款购买！")
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
                        df.at[pid,"bank"]+=edf.at[item,"per price"]*num
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
                if df.at[pid,"bank"]<edf.at[item,"per price"]*num:
                    print("error!")
                    t.sleep(1)
                else:
                    if item in df.at[pid,"stock"]:
                        df.at[pid,"stock"][item]+=num
                        df.at[pid,"bank"]-=edf.at[item,"per price"]*num
                    else:
                        df.at[pid,"stock"][item]=num
                        df.at[pid,"bank"]-=edf.at[item,"per price"]*num
                    break
        if choose=="quit":
            break
    return df

def shop(df,toydic,toydf,shoplist,pid):#超市
    item={}
    while True:
        num=ra.randint(0,len(toydic["toyname"])-1)
        if toydic["toyname"][num] not in item:
            item[toydf.at[num,"toyname"]]=toydf.at[num,"per price"]
        if len(item)>=shoplist:
            break
    print("有以下商品：",item)
    while True:
        buy=input("输入你要购买的商品名称或者输入quit退出")
        if buy in item and item[buy]<df.at[pid,"cash"]:
            df.at[pid,"cash"]-=item[buy]
            if buy in df.at[pid,"toy"]:
                df.at[pid,"toy"][buy]+=1
                item.pop[buy]
            elif buy not in df.at[pid,"toy"] and buy in item:
                df.at[pid,"toy"][buy]=1
                item.pop(buy)
        elif buy=="quit":
            break
        else:
            print("error!")
    return df

