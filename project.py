from tkinter import * 
from tkinter import ttk
import sqlite3
import threading
from kiteconnect import KiteConnect

import os
print("Using DB at:", os.path.abspath("stockmarket.db"))

root=Tk() 
root.geometry("600x350")
stop=False
def startThread():
    t1=threading.Thread(target=startScan)
    t1.start()
def stopScan():
    global stop
    stop=True
def startScan():
    widgets=scrollableFrame.winfo_children()
    i=0
    instruments=[]
    size=len(widgets)/6
    while(i<size):
        instruments.append("NSE:"+widgets[i*6]["text"])
        i+=1
    change=0
    while(True):
        quote=kite.quote(instruments)
        i=0
        global stop
        if(stop==True):
            stop=False
            break
        while(i<size):
            widgets[(i*6)+1]["text"]=quote[instruments[i]]["ohlc"]["high"]
            widgets[(i*6)+2]["text"]=quote[instruments[i]]["ohlc"]["low"]
            widgets[(i*6)+3]["text"]=quote[instruments[i]]["volume"]
            widgets[(i*6)+4]["text"]=quote[instruments[i]]["last_price"]
            change=((quote[instruments[i]]["last_price"]-quote[instruments[i]]["ohlc"]["close"])/quote[instruments[i]]["ohlc"]["close"])*100
            widgets[(i*6)+5]["text"]="{:.2f}".format(change)
            if(change>0):
                widgets[(i*6)+5].config(foreground="green")
            else:
                widgets[(i*6)+5].config(foreground="red")
            i+=1
def connectZerodha():
    global kite
    kite=KiteConnect(api_key="kjz4xgysne8a61xl")
    request_token=entryToken.get()
    data=kite.generate_session(request_token,api_secret="o25xaq54stwrnqmxsoqttb38kol6sne5")
    kite.set_access_token(data["access_token"])
    top.destroy()
    print(kite.profile()["user_name"])
def popup():
    global top,entryToken
    top=Toplevel(root)
    entryToken=ttk.Entry(top)
    entryToken.grid(row=0,column=0)
    Button(top,text="SUBMIT",command=connectZerodha).grid(row=0,column=1)
def addDb():
    conn = sqlite3.connect("stockmarket.db")
    stockList = stockName.get().split(",")
    for name in stockList:
        conn.execute("insert into stocks(name,indices) values('" + name + "','" + indices.get() + "')")
    conn.commit()
    conn.close()
    print("DB UPDATED")
def refreshTable(event):
    i=0
    clearWidgets()
    conn=sqlite3.connect("stockmarket.db")
    cursor=conn.execute("select * from stocks where indices='"+indices.get()+"'")
    for row in cursor:
        ttk.Label(scrollableFrame,text=row[0],width=15,font=("Times New Roman bold",10),borderwidth=2,relief="groove").grid(row=i,column=0)
        ttk.Label(scrollableFrame,text="",width=15,font=("Times New Roman bold",10),borderwidth=2,relief="groove").grid(row=i,column=1)
        ttk.Label(scrollableFrame,text="",width=15,font=("Times New Roman bold",10),borderwidth=2,relief="groove").grid(row=i,column=2)
        ttk.Label(scrollableFrame,text="",width=15,font=("Times New Roman bold",10),borderwidth=2,relief="groove").grid(row=i,column=3)
        ttk.Label(scrollableFrame,text="",width=15,font=("Times New Roman bold",10),borderwidth=2,relief="groove").grid(row=i,column=4)
        ttk.Label(scrollableFrame,text="",width=15,font=("Times New Roman bold",10),borderwidth=2,relief="groove").grid(row=i,column=5)
        i+=1
def clearWidgets():
    widgets = scrollableFrame.winfo_children()
    i=0
    while(i<len(widgets)):
        widgets[i].destroy()
        i+=1

topFrame=Frame(root)
Button(topFrame,text="CONNECT",command=popup).grid(row=0,column=0)
Label(topFrame,text="INDEX").grid(row=0,column=1) 
indices=ttk.Combobox(topFrame, values=["NIFTY 50","NIFTY NEXT 50","NIFTY BANK","NIFTY FINANCIAL SERVICES"],width=15,font=("Arial Bold",10))
indices.bind("<<ComboboxSelected>>",refreshTable)
indices.grid(row=0,column=2)
Label(topFrame,text="NAME").grid(row=0,column=3)
stockName=Entry(topFrame)
stockName.grid(row=0,column=4)
Button(topFrame,text="ADD TO DB",command=addDb).grid(row=0,column=5)
Button(topFrame,text="START",command=startThread).grid(row=0,column=6)
Button(topFrame,text="STOP",command=stopScan).grid(row=0,column=7)
topFrame.pack()


titleFrame=Frame(root)
Label(titleFrame,text="NAME",width=13,font=("Times New Roman bold",10)).grid(row=0,column=0)
Label(titleFrame,text="HIGH",width=13,font=("Times New Roman bold",10)).grid(row=0,column=1)
Label(titleFrame,text="LOW",width=13,font=("Times New Roman bold",10)).grid(row=0,column=2)
Label(titleFrame,text="VOLUME",width=13,font=("Times New Roman bold",10)).grid(row=0,column=3)
Label(titleFrame,text="LTP",width=13,font=("Times New Roman bold",10)).grid(row=0,column=4)
Label(titleFrame,text="CHANGE",width=13,font=("Times New Roman bold",10)).grid(row=0,column=5)
titleFrame.pack()

botFrame=Frame(root)
canvas=Canvas(botFrame)
scrollbar=ttk.Scrollbar(botFrame,orient="vertical",command=canvas.yview)
scrollableFrame=ttk.Frame(canvas)
scrollableFrame.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0,0),window=scrollableFrame,anchor="nw")
canvas.configure(width=580,yscrollcommand=scrollbar.set)
botFrame.pack()
canvas.pack(side="left",fill="both",expand=True)
scrollbar.pack(side="right",fill="y")

root.mainloop()
