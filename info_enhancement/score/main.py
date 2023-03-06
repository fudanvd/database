# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from transformers import logging
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM
from sklearn.neighbors import  KNeighborsClassifier
import joblib
import sys
import pandas as pd
import numpy as np

from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier


logging.set_verbosity_warning()

tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")

model = AutoModelForMaskedLM.from_pretrained("bert-base-chinese")


def get_vector(sentenceA):
    # Use a breakpoint in the code line below to debug your script.
    #print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    if len(sentenceA)>=500:
        sentenceA = sentenceA[0:500]
    # tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
    #
    # model = AutoModelForMaskedLM.from_pretrained("bert-base-chinese")


    text_dict = tokenizer.encode_plus(sentenceA, add_special_tokens=True, return_attention_mask=True)
    input_ids = torch.tensor(text_dict['input_ids']).unsqueeze(0)
    token_type_ids = torch.tensor(text_dict['token_type_ids']).unsqueeze(0)
    attention_mask = torch.tensor(text_dict['attention_mask']).unsqueeze(0)

    res = model(input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
    #print(1)
    #return res[0].detach().squeeze(0).numpy().tolist()[0]
    return res[0].detach().squeeze(0).numpy().tolist()[0]



if __name__ == '__main__':
    sentenceA = '四个格式字符串注入漏洞存在于Abode Systems, Inc.iota All-In-One Security Kit 6.9Z和6.9X的web界面/action/wirelessConnect功能。一个特别制作的HTTP请求可导致内存损坏、信息泄露和拒绝服务。攻击者可以通过认证的HTTP请求来触发这些漏洞。该漏洞产生于通过`default_key_id`HTTP参数的格式字符串注入，在`/action/wirelessConnect`处理器中使用。'
    x=[]
    y=[]
    with open(r"final.txt",'r',encoding="utf-8") as file:
        for line in file:
            line = line.strip('\n').split("||")
            if '-'in line[1]:
                continue
            x.append( get_vector(line[2]) )
            y.append(line[1])

        file.close()




    i = 3
    x_train = x[0:len(x)-10000]
    y_train = y[0:len(y)-10000]

    x_test = x[len(x)-10000:len(x)-1]
    y_test = y[len(y)-10000:len(y)-1]

    best_to_now = sys.maxsize
    flag = 0
    while i < 205:

        neigh=KNeighborsClassifier(n_neighbors=i)

        neigh.fit(x_train, y_train)


        out = neigh.predict(x_test)

        count = 0
        temp = 0.0
        while count < len(out):
            temp = temp + (float(out[count]) - float(y_test[count])) * (float(out[count]) - float(y_test[count]))
            count = count + 1
        if temp < best_to_now:
            flag = i
            best_to_now = temp



        i = i + 2
    neigh = KNeighborsClassifier(n_neighbors=flag)
    neigh.fit(x, y)
    joblib.dump(neigh , r'final.pkl')
    # joblib.dump(neigh , r'final.pkl')
    #
    # my_neigh = joblib.load(r'final.pkl')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
