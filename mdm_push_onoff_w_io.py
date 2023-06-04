# -*- coding:utf-8 -*-
import sys
import os
import datetime
import mysql.connector
from bs4 import BeautifulSoup as bs
import requests
import warnings
warnings.filterwarnings(action='ignore')

def check_status(enter,hostName):
    response = os.system("ping -n 1 " + hostName)
    if response == 0:
        print(enter+"_Network Active")
        Netstatus=1
    else:
        print(enter+"_Network Error")
        Netstatus=0
    return Netstatus



setdata={}
setdirpath = r"D:\push"

sdate=input("format=20210607190000, Sdate: ")
ddate=input("format=20210607210000, Ddate: ")






print("IODB > ", end="", flush=True)
N = [input() for _ in range(8)]
for n in N:
    setdata[n.split()[0]]=n[3:].strip()

for enter in setdata:
    config = {
        'user':setdata[enter][0],
        'password':setdata[enter][1].replace('\'',''),
        'host':setdata[enter][2],
        'db':setdata[enter][3]
        }

    Netstatus = check_status(enter,setdata[enter][2])
    if Netstatus == 0: continue

    try:
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        sql = """
SELECT * FROM $TABLE$ WHERE (Dtime, Id) IN (SELECT MAX(Dtime), Id FROM $TABLE$ WHERE Getdatetime >= {0} AND Getdatetime < {1} GROUP BY Id) AND reader NOT IN (SELECT reader FROM $TABLE$);
""".format(sdate,ddate)

        cur.excute(sql)
        data=cur.fetchall()

        with open(setdirpath+"\inout_result_"+sdate+"_"+ddate+".csv","a",encoding='utf-8-sig') as fp:
            for x in data:
                fp.write(str(x).replace('(','').replace(')','').replace("'","")+','+enter+'\n')
                fp.close()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()
        fp.close()







send_on=[]
send_off=[]

f=open(setdirpath + "\sending.csv","w+",encoding='utf-8-sig')
with open(setdirpath + "\inout_result_"+sdate+"_"+ddate+".csv","r",encoding='utf-8-sig') as fp:
    while line := fp.readline():
        line_split = line.replace(" ","").split(',')
        f.write(line_split[4]+","+str(int(line_split[2])%2)+"\n")
        if int(line_split[2])%2 : send_on.append(line_split[4])
        else: send_off.append(line_split[4])
f.close()
fp.close()

print("send_on")
print(send_on)
print("send_off")
print(send_off)






gdb = input("GDB > ").split()
config = {
        'user':gdb[0],
        'password':gdb[1].replace('\'',''),
        'host':gdb[2],
        'db':gdb[3]
        }

try :
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()

    sql="""
SELECT DUN.fDUN, U.m, D.i, D.aT FROM DUN AS DUN LEFT OUTER JOIN DU AS U ON DUN.oi = U.i LEFT (DUN.dUN = D.dUN) GROUP BY DUN.fDUN;
"""

    cur.execute(sql)
    data = cur.fetchall()

    with open(setdirpath + r"\userdevice_from_gdb.csv","w+",encoding='utf-8-sig') as fp:
        for x in data:
            fp.write(str(x).replace('(','').replace(')','').replace("'","")+','+'\n')
    fp.close()
except Exception as e:
    print(e)

finally:
    cur.close()
    conn.close()
    fp.close()







gdb = input("GWEB > ").split()

MEMBER_DATA = {
    'm_username': gdb[1],
    'm_password': gdb[2]
    }

with requests.Session() as s:
    response2 = s.post(gdb[0]+'/auth', data=MEMBER_DATA, verify=False)

bs_obj2 = bs(response2.content, 'html.parser')
#print(bs_obj2)

with open(setdirpath + r"\push_result.csv","w+",encoding='utf-8-sig') as pr:
    pr.write("모드,2,3,4,5\n")
    with open(setdirpath + r"\userdevice_from_gdb.csv","r",encoding='utf-8-sig') as fp:
        while line := fp.readline():
            split_uid = line.replace(" ","").split(",")
            if split_uid[1] in send_on:
                print(split_uid[1]+" "+split_uid[3])
                req= s.get(gdb[0]+"/mgr/device/mpolicyon/"+split_uid[3]+","+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"\n")

        fp.seek(0,0)

        while line := fp.readline():
            split_uid = line.replace(" ","").split(",")
            if split_uid[1] in send_off:
                print(split_uid[1]+" "+split_uid[3])
                req = s.get(gdb[0]+"/mgr/device/policyoff/"+split_uid[3], verify=False)


pr.write("OFF,"+split_uid[1]+","+split_uid[2]+","+split_uid[3]+","+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"\n")
    fp.close()
pr.close()
print("[push_result.csv] file created")

if os.path.exists(setdirpath+"\sending.csv"):
    os.remove(setdirpath+"\sending.csv")
    print("Temp file removed")
if os.path.exists(setdirpath+r"\userdevice_from_gdb.csv"):
    os.remove(setdirpath+r"\userdevice_from_gdb.csv")
    print("Temp file removed")

print("WORK DONE")
                
