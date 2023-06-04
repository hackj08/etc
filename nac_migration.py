# -*- coding:cp949 -*-
import os
import xlrd
import datetime


timenow=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

folder_path = os.path.dirname(os.path.abspath(__file__))

fline="IP,MAC,CUSTOM01,CUSTOM02,CUSTOM03,CUSTOM04,CUSTOM05,CUSTOM06,CUSTOM07,CUSTOM08,CUSTOM09,CUSTOM10,CUSTOM11,CUSTOM12,CUSTOM13"+"\n"
with open(folder_path+"\\update_"+timenow+".csv","a",encoding='cp949') as updatef:
    updatef.write(fline)

fline_insert"IP,MAC\n"
insertf=open(folder_path+"\\insert_"+timenow+".csv","a",encoding='cp949')
insertf.write(fline_insert)

insert_apnd=[]

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    if os.path.isfile(file_path):
        if file_path.find("geniannodemgmt")>0 or file_path.find("insert")>0 or file_path.find("update")>0:
            if file_path.find("geniannodemgmt")>0:
                gnpath=file_path
                print("gn path: ", gnpath)
            pass
        elif file_path.endswith(".xls"):
            print("file_path : ",file_path)
            print("file_name : ",filename)

            fpath=file_path
            workbook=xlrd.open_workbook(file_path)
            sheet = workbook.sheet_by_index(0)

            with open(folder_path+"\\update_"+timenow+".csv","a+",encoding='cp949') as output:
                for row_index in range(sheet.nrows):
                    if row_index == 0: continue
                    row = sheet.row_values(row_index)
                    line = row[0]+","+row[1].replace('-',':')+","+row[2]+","+row[3].replace(',','_')+","+row[4]+","+row[5]+","+row[6].replace(',','_')+","+row[7].replace(',','_')+","+row[8]+","+row[9]+","+row[10]+","+row[11].replace(',','_')+","+row[12].replace(',','_')+","+row[13]
                    output.write(line+,","+filename[:filename.rfind(".")]+"\n")

                output.seek(0)

                gn = open(gnpath,"r",encoding='cp949')
                output = open(folder_path+"\\update_"+timenow+".csv","r",encoding='cp949')

                for i, readline in enumerate(output.readlines()):
                    if i == 0: continue
                    line=readline.split(',')
                    #print(i, line)

                    count=0
                    gn.seek(0)
                    for j, gnline in enumerate(gn.readlines()):
                        if j == 0: continue

                        if gnline.find(line[0])>0 and gnline.find(line[1].replace('-',':'))>0:
                            count=count+1


                    if count == 0:
                        if line[1].find(':')>0:
                            insertf.write(line[0]+","+line[1]+"\n")


                output.close()
                gn.close()
                insertf.close()
