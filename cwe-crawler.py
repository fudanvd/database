from urllib import request
import re
import time
import random

ID=0
class CWECrawler(object):
    # 初始化
    # 定义初始页面url
    def __init__(self):
        self.url = 'https://cwe.mitre.org/data/definitions/{}.html'

    # 请求函数
    def get_html(self,url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50'}
        req = request.Request(url=url,headers=headers)
        res = request.urlopen(req)
        html = res.read().decode()
        # 直接调用解析函数
        self.parse_html(html)
    
    # 解析函数
    def parse_html(self,html):
        # 正则表达式
        re_bds = '<div id="Common_Consequences">.*?<i>(.*?)</i>.*?</div>'
        # 生成正则表达式对象
        pattern = re.compile(re_bds,re.S)
        impact = re.search(pattern,html)
        self.save_html(impact)


    #保存函数
    def save_html(self,impact):
        global ID
        with open('cwe-id.txt','a',encoding="utf-8") as file:
            if impact!=None:
                impact=impact.group(1)
                file.write(str(ID)+impact+'\n')
            else:
                file.write(str(ID)+"NULL"+'\n')
            file.close()
    
    # 主函数
    def run(self):
        global ID
        for num in range(1,1396):
            ID=ID+1
            url = self.url.format(num)
            self.get_html(url)
            time.sleep(random.uniform(0,1))

# 以脚本方式启动
if __name__ == '__main__':
    #捕捉异常错误
    try:
        crawler = CWECrawler()
        crawler.run()
    except Exception as e:
        print("错误:",e)
    
