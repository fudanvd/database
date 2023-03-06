import requests
from lxml import html
from bs4 import BeautifulSoup
import re
import datetime
import urllib.request as request


def get_num(soup):
    div_list = str(soup.find_all('div', class_="d-block d-lg-none no-wrap"))
    #print(div_list)
    open_num = re.findall("[0-9]{1,5} Open", div_list)
    closed_num = re.findall("[0-9]{1,5} Closed", div_list)
    o_num = int(str(open_num[0]).replace(' Open', ''))
    c_num = int(str(closed_num[0]).replace(' Closed', ''))
    number_sum = o_num + c_num
    return number_sum  # 我们得到了对于这单个keyword，可能要爬取的总数


def add_url(repository_url, pg_num, key_word, dest_time):
    basic_url = repository_url + "pulls?page=" + str(pg_num) + "&q=" + key_word
    str_html = requests.get(url=basic_url)
    soup = BeautifulSoup(str_html.text, 'lxml')

    info_div = str(soup.find_all('span', class_="opened-by"))
    # print(info_div)
    numbering_str = re.findall('#[0-9]{1,7}', info_div)
    # Dec 16, 2022
    date_str = re.findall(
        '(((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\.?)))( ?)(\d+)((st|nd|rd|th)?),( ?)(\d{2,})', info_div)

    count = 0
    global pull_numbers
    while count < len(date_str):
        single_date_str = date_str[count][0] + ' ' + date_str[count][5] + ', ' + date_str[count][9]
        single_date = datetime.datetime.strptime(single_date_str, "%b %d, %Y")
        single_numbering_str = numbering_str[count].replace("#", '')
        count = count + 1
        duration = (single_date - dest_time).days
        #print(duration)
        global date_flag
        if duration < -100:
            date_flag = 1
            break
        if (duration < 30) and (duration > -100):
            possible_pull_url.append(repository_url + "pull/" + single_numbering_str)

    return count


def get_possible_pulls_url(repository_url, key_word, dest_time):
    basic_url = repository_url + "pulls?page=1&q=" + key_word

    str_html = requests.get(url=basic_url)
    soup = BeautifulSoup(str_html.text, 'lxml')
    number_sum = get_num(soup)

    my_count = 0
    pg_num = 1

    while my_count < number_sum:
        my_count = my_count + add_url(repository_url, pg_num, key_word, dest_time)
        pg_num = pg_num + 1
        if date_flag == 1:
            my_count = number_sum
            break
        #for url in possible_pull_url:
            #print(url)
    return


def get_commit_message(pull_single):
    basic_url = pull_single['origin_url'] + "/commits"
    html = requests.get(basic_url)
    soup = BeautifulSoup(html.text, 'lxml')
    commit_id_div = soup.find_all('a',class_="tooltipped tooltipped-sw btn-outline btn BtnGroup-item text-mono f6")
    #print(commit_id_div)
    commit_id = re.findall('/commits/[0-f]{1,100}',str(commit_id_div))
    #print(html.text)
    reg = re.compile('<[^>]*>')
    for commit in commit_id:
        commit_structure = {
            "commit_id":None,
            "description":[],
            "position":[],
            "code":
            {
                "cut":[],
                "add":[]
            }
        }
        commit_url = pull_single['origin_url'] + commit
        commit_html = requests.get(commit_url)
        commit_structure["commit_id"] = commit_url
        #print(commit_html.text)
        #print(commit_url)
        commit_soup = BeautifulSoup(commit_html.text, 'lxml')

        commit_descriptions = commit_soup.find_all("div",class_="commit-title markdown-title")
        for commit_description in commit_descriptions:
            commit_structure["description"].append(reg.sub('',str(commit_description) ))

        commit_positions = commit_soup.find_all("span",class_="Truncate")
        for commit_position in commit_positions:
            commit_structure["position"].append(reg.sub('',str(commit_position).replace('\n','') ))

        commit_code_cuts = commit_soup.find_all("span",class_="blob-code-inner blob-code-marker js-code-nav-pass js-skip-tagsearch")
        for commit_code_cut in commit_code_cuts:
            if 'data-code-marker="-"' in str(commit_code_cut):
                commit_structure["code"]["cut"].append(reg.sub("",str(commit_code_cut)))

        commit_code_adds = commit_soup.find_all("span",class_="blob-code-inner blob-code-marker js-code-nav-pass")
        for commit_code_add in commit_code_adds:
            if 'data-code-marker="+"' in str(commit_code_add):
                commit_structure["code"]["add"].append(reg.sub('',str(commit_code_add) ))



        pull_single['commit_code'].append(commit_structure)

    return pull_single

def get_pull_message(url):
    pull_single = {
        'origin_url': url,
        'comment':[],
        'commit_code':[]
    }
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    title_div = soup.find_all("bdi", class_="js-issue-title markdown-title")[0]
    comment_div = soup.find_all('div',class_="comment-body markdown-body js-comment-body soft-wrap user-select-contain d-block")
    reg = re.compile('<[^>]*>')
    title_text = reg.sub('', str(title_div))
    pull_single['title'] = title_text
    for comment in comment_div:
        temp = reg.sub('',str(comment))
        pull_single['comment'].append(temp.replace('\n',' '))

    #print(pull_single)
    pull_single = get_commit_message(pull_single)
    print(pull_single)

    return pull_single


#if __name__ == "__main__":
def get_key_pull(key_wordes,repository_url,dest_time):
    #key_wordes = ['OOM', 'NPE']
    #dest_time = datetime.datetime.strptime("Mar 3, 2022", "%b %d, %Y")
    global headers
    global date_flag
    date_flag = 0

    headers = {'User-Agent':'Mozilla/5.0',
           'Authorization': 'token ef802a122df2e4d29d9b1b868a6fefb14f22b272',
           'Content-Type':'application/json',
           'Accept':'application/json'
          }
    #repository_url = 'https://github.com/elastic/elasticsearch/'
    global possible_pull_url
    possible_pull_url = []
    i = 0
    for key_word in key_wordes:


        get_possible_pulls_url(repository_url,key_word, dest_time)


    pull = []
    for url in possible_pull_url:
        #print(url)
        try:
            temp = get_pull_message(url)
            pull.append(temp)
        except Exception as e:
            print("an error occured, main due to the bad internet! We are attemptting to try again!")
            try:
                temp = get_pull_message(url)
                pull.append(temp)
            except Exception as e:
                print(e)
            continue
        # 现在我们有了过滤日期和关键词的url
        # https://github.com/elastic/elasticsearch/pull/92392
        # https://github.com/elastic/elasticsearch/pull/90990
        # https://github.com/elastic/elasticsearch/pull/90632
    return pull
    #get_pull_message("https://github.com/elastic/elasticsearch/pull/92392")
