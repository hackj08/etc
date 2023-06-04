# -*- coding:utf-8 -*-
import sys
import os
import datetime
import mysql.connector

def check_status(enter,hostName):
    response = os.system("ping -n 1 " + hostName)
    if response == 0:
        print(enter+"_Network Active")
        Netstatus=1
    else:
        print(enter+"_Network Error")
        Netstatus=0
    return Netstatus


setdata=0
sitel=['','','','','','','','']

sdate=input("format=20210607190000, Sdate: ")
ddate=input("format=20210607210000, Ddate: ")

setdirpath=r"D:\"
with open(setdirpath+"inout_result_"+sdate+"_"ddate+".csv","a",encoding='utf-8-sig') as fp:
    fp.write('1,2,3,4,5,6,7,8,9,10'+'\n')
    fp.close()

for site in sitel:
    setdata[site]=[x for x in input("%s: "%site).split()]

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

        with open(setdirpath+"inout_result_"+sdate+"_"+ddate+".csv","a",encoding='utf-8-sig') as fp:
            for x in data:
                fp.write(str(x).replace('(','').replace(')','').replace("'","")+','+enter+'\n')
                fp.close()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()
        fp.close()
     
