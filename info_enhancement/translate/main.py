#coding:utf-8
import os
import json

def get_files():
    for filepath, dirnames, filenames in os.walk("C:\\Users\\HP1\\Desktop\\数据库搭建\\nvd_vulnerabilities"):
        for filename in filenames:
            dealwith(os.path.join(filepath, filename))

filename6 = "C:\\Users\\HP1\\Desktop\\数据库搭建\\CVE Des_CN.txt"

def dealwith(filename):
    with open(filename) as load_f:
        load_dict = json.load(load_f)
    
    with open(filename6, 'a') as f1:
        f1.write(load_dict['CVE ID'] + "||")
        if isinstance(load_dict['CVE description'], str):
            f1.write(load_dict['CVE description'])
        else:
            f1.write("NULL")
        f1.write("\n")

get_files()

