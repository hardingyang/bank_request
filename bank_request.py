from bs4 import BeautifulSoup
from urllib import request
from urllib import parse
import pandas as pd
import csv

#每次运行，不能打开data,csv文件，不然会bug，然后每次重新运行都会覆盖原来的数据，所以得自己注意保存
#我是懒得改了，抱歉啊
with open('data.csv','w',newline='') as file:
    writer=csv.writer(file)
    writer.writerow(['货币名称','现汇买入价','现钞买入价','现汇卖出价','现钞卖出价','中行折算价','发布时间'])
url = "https://srh.bankofchina.com/search/whpj/search_cn.jsp"
Form_Data = {}
Form_Data['erectDate'] = '2019-12-17'   #设置起始时间
Form_Data['nothing'] = '2019-12-17' #设置终止时间
Form_Data['pjname'] = '美元'  #设置要取的排位选择
Form_Data['page']=''

#要爬出最新的一条，你就将时间段设置为同一天，第一条就是最新的

page=2   #设置这个时段，里面要爬取的页面，页面数不能超过web页最大页数
for p in range(1,page):
    Form_Data['page']=str(p)
    data = parse.urlencode(Form_Data).encode('utf-8')
    html = request.urlopen(url,data).read()
    soup = BeautifulSoup(html,'html.parser')

    # 解析数据
    div = soup.find('div', attrs = {'class':'BOC_main publish'})
    table = div.find('table')
    tr = table.find_all('tr')
    for index in range(1,len(tr)-1):
        td=tr[index].find_all('td')
        row=[]
        for i in range(len(td)):
            row.append(td[i].get_text())
        with open('data.csv', 'a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)

    print("完成第"+str(p)+"页")
print("爬取完成！！！")

csv = pd.read_csv('data.csv', encoding='gbk')
csv.to_excel('data-exl.xlsx',sheet_name='data')
print("转换excel完成")