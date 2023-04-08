# coding=utf-8
import time
import urllib3
import requests

source_filepath = "C:\\Users\\HP1\\Desktop\\Reference.txt"
des_filepath = "C:\\Users\\HP1\\Desktop\\commit_\\"

def get_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.Session()
    s.keep_alive = False
    s.verify = False
    urllib3.disable_warnings()
    proxies = {
        'http': 'http://127.0.0.1:7890/',
        'https': 'http://127.0.0.1:7890/'
    }
    res = s.get(url=url, headers=headers, proxies=proxies)
#    time.sleep(1)
    return res.text

with open(source_filepath,'r') as f1:
    count = 0
    while True:
        line = f1.readline()
        if not line: break
        if line.find("github") != -1 and line.find("commit") != -1:
            if line.find("#diff") != -1:
                line = line.split("#diff")[0]
            line = line.rstrip('\n')
            url = line.split("||")[1] + ".diff"
            cve_filepath = des_filepath + line.split("||")[0] + ".txt"
            try:
                text = get_url(url)
            except:
                try:
                    text = get_url(url)
                except:
                    print(line.split("||")[0] + " error")
                    continue
            with open(cve_filepath,'w') as f2:
                f2.write(text.encode('utf-8'))
            count += 1
    print("%s commits in total" % count)



        
