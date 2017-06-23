#coding=utf-8
import sys
import csv
import codecs
import time
reload(sys)
sys.setdefaultencoding( "utf-8" )
import re
import urllib2
from bs4 import BeautifulSoup


cookie='''ll="108296"; bid=3ulp-KToDD0; __yadk_uid=nOCwArTSKmqGU9Qqk8ANJH87IL0YQPva; ps=y; ct=y; _ga=GA1.2.356485403.1492179890; gr_user_id=55c2d769-6f22-4b7c-b6f2-9a8bae61189f; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1497081579%2C%22https%3A%2F%2Fwww.douban.com%2Fgroup%2Fblabla%2F%3Fref%3Dsidebar%22%5D; ap=1; dbcl2="143223369:GAcRphtZWtg"; ck=s_vv; _vwo_uuid_v2=094590DC1A892202A3B94439703D8891|4f5a2d71ae7963310fb5d9c34de6d705; __utmt=1; _pk_id.100001.4cf6=786a5183f2701f88.1492179890.47.1497083150.1497018683.; _pk_ses.100001.4cf6=*; __utma=30149280.356485403.1492179890.1497065485.1497081232.244; __utmb=30149280.97.4.1497082942394; __utmc=30149280; __utmz=30149280.1496983387.239.27.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=30149280.14322; __utma=223695111.533452423.1492179890.1497017029.1497081579.47; __utmb=223695111.0.10.1497081579; __utmc=223695111; __utmz=223695111.1497081579.47.35.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/group/blabla/; push_noty_num=0; push_doumail_num=0'''
header = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
'Connection': 'keep-alive',
# 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Cookie': cookie}

c=open("wonderwoman.csv","ab")
c.write(codecs.BOM_UTF8)
writer=csv.writer(c)
count=0
starttime=time.time()
writer.writerow(['movieID','ID','Score','Comment','Time'])
for id in [1578714]:
    for i in range(0,100):
        i=i*20
        req=urllib2.Request("https://movie.douban.com/subject/"+str(id)+"/comments?start="+str(i)+"&limit=20&sort=new_score&status=P",headers=header)
        try:
            r = urllib2.urlopen(req,timeout=10)
            html = r.read()
        except Exception,e:
            time.sleep(3)
            continue
        soup=BeautifulSoup(html,"lxml")
        for temp in soup.find_all('div',{'class':'comment'}):
            count=count+1
            for temp1 in temp.find_all('span',{'class':'comment-info'}):
                print temp1.a.string
                try:
                    k=temp1.find('span',{'class':re.compile("rating$")}).get('class')[0]
                    print k
                except Exception, e:
                    time.sleep(0.01)
            temp2=temp.find('span',{'class':'comment-time'})
            print temp.p.string
            print temp2.string.strip()
            rlist=[]
            rlist.append(id)
            rlist.append(temp1.a.string.strip())
            try:rlist.append(k.split("r")[1])
            except Exception,e:rlist.append(0)
            rlist.append(temp.p.string)
            rlist.append(temp2.string)
            writer.writerow(rlist)
            # words = pseg.cut(temp.get('data-comment'))
            # for key in words:
            #     print key.word, key.flag
        print "page"+str(i/20)
        time.sleep(0.22)
c.close()
print count
endtime=time.time()
print (endtime-starttime)

