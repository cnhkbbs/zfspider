# -*- coding:utf-8 -*-
# --------------------
# 20230520
# by sboxm
# --------------------
# 结果处理
from bs4 import BeautifulSoup as bf


def CookFood(username):
    try:
        with open(username + '.txt', 'r', encoding='utf-8') as file:
            score_response = file.read()
    except FileNotFoundError:
        return "返回结果失败，系统中没有对应记录！"
    except Exception as e:
        return "未知错误：" + str(e)
    soup = bf(score_response, 'html.parser')
    score_table = soup.find('table', {"class": "datelist"})
    html_header = '<!DOCTYPE html><html><head><meta charset="utf-8" /><title></title><style>td{border: 1px solid black!important;}</style></head><body>'
    html_footer = '	</body></html>'
    return html_header+str(score_table)+html_footer
