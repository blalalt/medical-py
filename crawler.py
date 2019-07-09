import time
import requests
import lxml
import os
import re
from bs4 import BeautifulSoup

question_list = r'http://ask.39.net/news/{}-{}.html'

base_url = r'http://ask.39.net'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 QQBrowser/10.4.3588.400'}

def get_html(url, headers=None):
    if not headers: headers=HEADERS
    return requests.get(url, headers=HEADERS).text


def parser_anwser_data(html: str):
    bs = BeautifulSoup(html, 'lxml')
    try:
        txt_ms = bs.select_one(selector='p.txt_ms').string
        sele_txt = bs.select_one(selector='p.sele_txt').string
    except Exception:
        return None, None
    return txt_ms, sele_txt


def parser_link_data(html: str):
    bs = BeautifulSoup(html, 'lxml')
    q_list = bs.select(selector='p.p1 a')
    for q in q_list:
        link = q['href']
        question = q.string
        yield link, question

def parser_link():
    base = r'http://ask.39.net/news/321-{}.html'
    for qu_page in range(1, 1000):
        url = base.format(str(qu_page))
        print(url)
        html = get_html(url)
        # print(url, html)
        for link, question in parser_link_data(html):
            abs_link = base_url + link
            # time.sleep(0.5)
            page_html = get_html(abs_link)
            detail_question, anwser = parser_anwser_data(page_html)
            if None in [detail_question, anwser]: continue
            print(detail_question, anwser)
            question = re.sub(',', '，', question)
            detail_question = re.sub(',', '，', str(detail_question).strip())
            # detail_question = re.sub(r'\n', '', detail_question)
            anwser = re.sub(',', '，', str(anwser).strip())
            # anwser = re.sub(r'\n', '', anwser)
            yield abs_link, question, detail_question, anwser
    
    

if __name__ == "__main__":
    with open('question_answer.txt', 'w', encoding='utf8') as f:
        for d in parser_link():
            print(d)
            f.writelines(','.join(list(d)) + '\n')
