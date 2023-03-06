import json
import os
from delstop import *
from bayes import *
from tfidf import *

def judgeCWEID(id):
    X_test = tfidf_matrix[id]
    CVEcatagory = bayesResult(final_model, X_test)
    return CVEcatagory

file_name_list = os.listdir('nvd_vulnerabilities')
needjudge_file_name_list = []

corpus = []
catagories = []

for file_name in file_name_list:
    with open('nvd_vulnerabilities/' + file_name, 'r', encoding='utf-8') as fp:
        json_data = json.load(fp)
        if "CVE description" in json_data.keys():
            corpus.append(wash_sentence(json_data["CVE description"]))

tfidf_matrix = tfidf_util(corpus).todense()
X = np.array(tfidf_matrix, dtype=np.float32)

for i in range(len(file_name_list)):
    with open('nvd_vulnerabilities/' + file_name_list[i], 'r', encoding='utf-8') as fp:
        json_data = json.load(fp)
        if "CVE description" in json_data.keys():
            if "CWE IDs" not in json_data.keys():
                needjudge_file_name_list.append(i)
                X = np.delete(X, i, axis=0)
            elif len(json_data["CWE IDs"]) == 0:
                needjudge_file_name_list.append(i)
                X = np.delete(X, i, axis=0)
            elif "other" in json_data["CWE IDs"][0].lower() or "noinfo" in json_data["CWE IDs"][0].lower():
                needjudge_file_name_list.append(i)
                X = np.delete(X, i, axis=0)
            else:
                CWEID = eval(json_data["CWE IDs"][0].split('-')[-1])
                catagories.append(CWEID)

Y = np.array(catagories, dtype=np.int32)
final_model = trainModel(X, Y)

CWE_dict = {}

for needjudge_file_name_id in needjudge_file_name_list:
    CWEID = judgeCWEID(needjudge_file_name_id)
    CWE_dict[file_name_list[needjudge_file_name_id]] = "CWE-" + str(CWEID)

with open('result.json','w+') as f:
    json.dump(CWE_dict, f)
