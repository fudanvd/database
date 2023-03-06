import nltk
from string import punctuation
from nltk.corpus import stopwords
import re


if __name__ == '__main__': 
    set(stopwords.words('english'))
    stop_words = set(stopwords.words('english'))
    with open('cwe-id.txt', 'r', encoding="utf-8") as file:
        txt_tables = file.readlines()
    file.close()     
                    
    with open('CVE_CWE_Des.txt', 'r', encoding="utf-8") as file_1,open('cve_impact.txt', 'a', encoding="utf-8") as file_2:
        line=file_1.readline()
        while line:
            a=line.split("||")
            if a[1][:3]=="CWE":
                num=[]
                weakness=""
                num=re.findall("\d+", a[1])
                for i in range(len(num)):
                    index=int(num[i])
                    words=nltk.word_tokenize(txt_tables[index-1])
                    filtered_sentence = []
                    for w in words:
                        if w not in stop_words and w not in punctuation:
                            filtered_sentence.append(w)
                    words.clear()
                    for w in filtered_sentence:
                        words.append(w)
                    filtered_sentence.clear()
                    for word in words:
                        if word in a[2]:
                            weakness=weakness+word+";"
                    if weakness=="":
                        for word in words:
                            weakness=weakness+word+";"
                    file_2.write(a[0]+"||"+weakness+'\n')
            else:
                file_2.write(a[0]+"||"+"NULL"+'\n')
            line=file_1.readline()
    file_1.close()
    file_2.close()
    




