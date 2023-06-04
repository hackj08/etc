#-*- coding:utf-8 -*-
import sys
import os


finding_word=['','','']

targetdir=r"D:\target\"
savedir=r"D:\result\"

if not(os.path.isdir(savedir)):
    os.makedirs(savedir)
files=os.listdir(targetdir)

for file in files:
    target=targetdir+file
    print("---target file: "  target)

    with open(target,"r", encoding='utf-8-sig') as fp:
        for fw in finding_word:
            print("---UserID > "+fw)
            savefile=savedir+fw+".csv"
            #savefile=savedir+"result.csv"
            result_f=open(savefile,"a",encoding='utf-8-sig')
            while 1:
                line = fp.readline()
                if not line: break

                if line.find(',') < line.find(fw) and line.find(fw) < 20:
                    result_f.write(line)
            result_f.close()
            fp.seek(0)
    fp.close()
