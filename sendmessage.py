# -*- coding:utf-8 -*-

from urllib import parse
import requests
import datetime
import mysql.connector
import sys


id="3205"
day = str(int(datetime.datetime.now().strftime("%Y%m%d"))+1)



config={
    'user': ,
    'password': ,
    'host': ,
    'db':
    }


try:
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()

    sql="SQL='"+day+"';"

    cur.execute(sql)
    data= cur.fetchall()

    if len(data) is 0:
        sys.exit()
    else:
        salad=data[-1][-2]
        url=parse.urlparse('URL'+salad)
        query=parse.parse_qs(url.query)
        result=parse.urlencode(query, doseq=True)
        requests.get("URL"+id+"&"+result, verify=False)

except Exception as e:
    print(e)

finally:
    cur.close()
    conn.close()
    
