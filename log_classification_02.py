#-*- coding:utf-8 -*-
import sys
import os
import datetime


print("Starting : "+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

find_word=[]
while(1):
    print("Input Number : ", end="", flush=True)
    a=input()

    if(a)=="":
        break

    if a.find(",")>0:
        b=a.replace(" ","").replace("'","")
        b=b.split(",")
        finding_word=finding_word+b
        continue

    finding_word.append(a)


print("FIND : ",finding_word)

targetdir=r"D:\target\"
savedir=r"D:\result\"

if not(os.path.isdir(savedir)):
    os.makedirs(savedir)
files=os.listdir(targetdir)

resultfilename=savedir+"result.csv"


for file in files:
    result_f=open(resultfilename,"a",encoding='utf-8-sig')
    target=targetdir+file
    print("---target file : " + target)

    with open(target,"r",encoding='utf-8-sig') as fp:
        while 1:
            line = fp.readline()
            if not line: break

            startno=line.find(',',0)
            endno=line.find(',',startno+1)
            uid=line[tartno+1:endno]

            if uid in finding_word:
                result_f.write(line)
                #filename=savedir+uid+".csv"
                #result_f=open(filename,"a",encoding='utf-8-sig')
            fp.close()
            result_f.close()

print("Work Done : "+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
