import os
import json


def get_files():
    for filepath, dirnames, filenames in os.walk("D:\\漏洞数组库\\nvd_vulnerabilities"):
        for filename in filenames:
            dealwith(os.path.join(filepath, filename))


filename1 = "D:\\漏洞数组库\\CVE.txt"
filename2 = "D:\\漏洞数组库\\Patches.txt"
filename3 = "D:\\漏洞数组库\\Reference.txt"
filename4 = "D:\\漏洞数组库\\Versions.txt"
filename5 = "D:\\漏洞数组库\\CWEIDs.txt"

def dealwith(filename):
    with open(filename) as load_f:
        load_dict = json.load(load_f)
    with open(filename1, 'a') as f1:
        f1.write(load_dict['CVE ID'] + "||")
        if isinstance(load_dict['CVE ASSIGNER'], str):
            f1.write(load_dict['CVE ASSIGNER'])
        else:
            f1.write("NULL")
        f1.write("||")
        if isinstance(load_dict['vendor'], str):
            f1.write(load_dict['vendor'])
        else:
            f1.write("NULL")
        f1.write("||")
        if isinstance(load_dict['product'], str):
            f1.write(load_dict['product'])
        else:
            f1.write("NULL")
        f1.write("||")
        if isinstance(load_dict['CVSS (version 3.x) score'], str):
            f1.write(load_dict['CVSS (version 3.x) score'])
        else:
            f1.write("NULL")
        f1.write("||")
        if isinstance(load_dict['CVSS (version 2.x) score'], str):
            f1.write(load_dict['CVSS (version 2.x) score'])
        else:
            f1.write("NULL")
        f1.write("||")
        if isinstance(load_dict['publishedDate'], str):
            f1.write(load_dict['publishedDate'])
        else:
            f1.write("NULL")
        f1.write("||")
        if isinstance(load_dict['lastModifiedDate'], str):
            f1.write(load_dict['lastModifiedDate'])
        else:
            f1.write("NULL")
        f1.write("||")
        if isinstance(load_dict['CVE description'], str):
            f1.write(load_dict['CVE description'])
        else:
            f1.write("NULL")
        f1.write("||")
        if isinstance(load_dict['fix'], str):
            f1.write(load_dict['fix'])
        else:
            f1.write("NULL")
        f1.write("\n")

    with open(filename2, 'a') as f2:
        for patch in load_dict['patches']:
            f2.write(load_dict['CVE ID'] + "||" + patch + "\n")
    with open(filename3, 'a') as f3:
        for reference in load_dict['references']:
            f3.write(load_dict['CVE ID'] + "||" + reference + "\n")
    with open(filename4, 'a') as f4:
        for version in load_dict['affected versions']:
            f4.write(load_dict['CVE ID'] + "||" + version + "\n")

    with open(filename5, 'a') as f5:
        for cweid in load_dict['CWE IDs']:
            f5.write(load_dict['CVE ID'] + "||" + cweid + "\n")



get_files()
