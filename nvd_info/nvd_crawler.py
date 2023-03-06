import os
import datetime
import json
import zipfile
import urllib.request


class Crawler:
    # 初始化
    def __init__(self):
        self.zip_path = os.path.join(os.path.abspath(os.path.join(
            os.path.dirname(__file__), ".")), "nvd_zip")  # nvd原始数据压缩包文件夹的路径
        self.data_path = os.path.join(os.path.abspath(os.path.join(
            os.path.dirname(__file__), ".")), "nvd_data")  # nvd原始数据文件夹的路径
        self.vulnerabilities_path = os.path.join(os.path.abspath(os.path.join(
            os.path.dirname(__file__), ".")), "nvd_vulnerabilities")  # nvd漏洞数据文件夹的路径

    # 下载nvd原始数据的压缩包
    def zip_downloader(self):
        error_urls = []
        print("zip downloading...")
        cur_year = datetime.datetime.now().year
        for year in range(2002, cur_year):
            file_path = os.path.join(
                self.zip_path, f'nvdcve-1.1-{year}.json.zip')
            if not os.path.exists(file_path):
                url = f'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{year}.json.zip'
                try:
                    urllib.request.urlretrieve(url, file_path)
                    print(f"{year} finished")
                except Exception:
                    print("download error:", url, "try later")
                    error_urls.append(url)
        while error_urls:
            url = error_urls.pop()
            try:
                f = urllib.request.urlopen(url)
                data = f.read()
                with open(file_path, 'wb') as zip_file:
                    zip_file.write(data)
                print(f"{year} finished")
            except Exception:
                print("download error:", url, "try later")
                error_urls.append(url)

    # 解压nvd原始数据
    def unzip(self):
        dirs = os.listdir(self.zip_path)
        for file in dirs:
            if file.endswith('.zip'):
                zip = zipfile.ZipFile(
                    os.path.join(self.zip_path, file))
                for name in zip.namelist():
                    zip.extract(name, self.data_path)
                    print(name + "unzip done")
                zip.close()
                os.remove(os.path.join(self.zip_path, file))

    # 分析references中的链接

    def patch_handler(self, ref) -> bool:
        # 如果是一个commit链接
        if '/commit' in ref['url']:
            return True
        # 如果被标记为patch链接
        if 'Patch' in ref['tags']:
            return True
        else:
            return False

    # 解析nvd的json文件
    def nvd_parser(self, path: str):
        print("processing " + path)
        nvd_json = dict()
        with open(path, 'r', encoding='utf-8') as nvd_file:
            nvd_json = json.load(nvd_file)
        cve_items = nvd_json["CVE_Items"]
        for item in cve_items:
            cve_assigner = item["cve"]["CVE_data_meta"]["ASSIGNER"]
            cve_id = item["cve"]["CVE_data_meta"]["ID"]
            cpe_list = item["configurations"]["nodes"]
            cur_vendor = ""  # 此CVE漏洞对应的厂商名称
            cur_product = ""  # 此CVE漏洞对应的组件名称
            cur_cpes = list()  # 此CVE漏洞对应的所有CPE条目信息
            for cpe in cpe_list:
                if cpe['operator'] == 'OR':
                    for cpe_match in cpe['cpe_match']:
                        if cpe_match['vulnerable']:
                            if cur_vendor == "":
                                cur_vendor = cpe_match['cpe23Uri'].split(":")[
                                    3].lower()
                            if cur_product == "":
                                cur_product = cpe_match['cpe23Uri'].split(":")[
                                    4].lower()
                            # 获取CPE条目信息
                            if cpe_match['cpe23Uri'] not in cur_cpes:
                                cur_cpes.append(cpe_match['cpe23Uri'])
                else:
                    for child in cpe['children']:
                        for cpe_match in child['cpe_match']:
                            if cpe_match['vulnerable']:
                                if cur_vendor == "":
                                    cur_vendor = cpe_match['cpe23Uri'].split(":")[
                                        3].lower()
                                if cur_product == "":
                                    cur_product = cpe_match['cpe23Uri'].split(":")[
                                        4].lower()
                                # 获取CPE条目信息
                                if cpe_match['cpe23Uri'] not in cur_cpes:
                                    cur_cpes.append(cpe_match['cpe23Uri'])
            # cwe id信息
            cwe_id_list = []
            for cwe_value_dict in item["cve"]["problemtype"]["problemtype_data"][0]["description"]:
                cwe_id_list.append(cwe_value_dict["value"])
            # references信息
            references = item["cve"]["references"]["reference_data"]
            nvd_links = []
            patches = []
            for ref in references:
                nvd_links.append(ref["url"])
                # patch分析
                if self.patch_handler(ref):
                    patches.append(ref['url'])
            # cvss得分
            if "baseMetricV3" in item["impact"].keys():
                cvss_score_v3 = item["impact"]["baseMetricV3"]["cvssV3"]["baseScore"]
            else:
                cvss_score_v3 = None
            if "baseMetricV2" in item["impact"].keys():
                cvss_score_v2 = item["impact"]["baseMetricV2"]["cvssV2"]["baseScore"]
            else:
                cvss_score_v2 = None
            # 描述信息，添加初步的特殊字符的处理
            nvd_description = item["cve"]["description"]["description_data"][0]["value"]
            nvd_description.replace('\\', "\\\\")
            nvd_description.replace('\"', '\\"')
            nvd_description.replace('\'', "\\'")

            # 保存结果的字典
            cve_info = {}
            # cve信息结构
            cve_info["CVE ID"] = cve_id
            cve_info["CVE ASSIGNER"] = cve_assigner
            # 厂商、组件名称
            cve_info["vendor"] = cur_vendor
            cve_info["product"] = cur_product
            # 影响版本信息
            cve_info["affected versions"] = cur_cpes
            # CVSS评分、CWE ID
            cve_info["CVSS (version 3.x) score"] = cvss_score_v3
            cve_info["CVSS (version 2.x) score"] = cvss_score_v2
            cve_info["CWE IDs"] = cwe_id_list
            # 日期信息
            cve_info["publishedDate"] = item["publishedDate"][0:10]
            cve_info["lastModifiedDate"] = item["lastModifiedDate"][0:10]
            cve_info["CVE description"] = nvd_description
            cve_info["references"] = nvd_links
            cve_info["patches"] = patches
            cve_info["fix"] = None
            # 保存至json文件中
            try:
                json_path = os.path.join(
                    self.vulnerabilities_path, cve_id + ".json")
                if not os.path.exists(json_path):
                    with open(json_path, 'w', encoding="utf-8") as json_file:
                        json.dump(cve_info, json_file,
                                  ensure_ascii=False, indent=4)
            except:
                print(cve_id + "process error !")


if __name__ == '__main__':  # 确保作为脚本执行
    crawler = Crawler()
    if not os.path.exists(crawler.zip_path):
        os.makedirs(crawler.zip_path, mode=0o777)
    crawler.zip_downloader()
    if not os.path.exists(crawler.data_path):
        os.makedirs(crawler.data_path, mode=0o777)
    crawler.unzip()
    if not os.path.exists(crawler.vulnerabilities_path):
        os.makedirs(crawler.vulnerabilities_path, mode=0o777)
    for root, dirs, files in os.walk(crawler.data_path):
        for file in files:
            path = os.path.join(root, file)
            crawler.nvd_parser(path)
    os.rmdir(crawler.zip_path)
