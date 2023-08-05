# -*- coding:utf-8 -*-
# --------------------
# 20230520
# by sboxm
# --------------------
# fastapi服务

import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import datetime
import cookfood
import spider
from pydantic import BaseModel

app = FastAPI()

# 读取主页
with open('public/index.txt', 'r', encoding='utf-8') as index:
    index_content = index.read()


# 控制台信息
def print_INFO(message):
    print('[' + datetime.datetime.now().strftime('%H:%M:%S') + ']' + message)


def print_ERROR(error):
    print('[' + datetime.datetime.now().strftime('%H:%M:%S') + ']' + "\033[1;31m" + error + " \033[0m")


# 执行任务
async def do_mission(uname, pwd, cname, host, header):
    try:
        spider.zf_spider(uname, pwd, cname, int(host), int(header))
    except Exception:
        print_ERROR("Unknown exceptions" + str(Exception))


# 创建数据类型
class ResultModel(BaseModel):
    name: str


@app.get("/")
async def index():
    return HTMLResponse(content=index_content)


@app.post("/hi")
async def hi():
    return {"msg": "Hi", "code": 200}


@app.post("/submit")
async def submit(name: str = Form(...), password: str = Form(...), chinesename: str = Form(...), host: str = Form(...),
                 header: str = Form(...)):
    await do_mission(name, password, chinesename, host, header)
    return HTMLResponse(content="<a href='../'>提交成功，点我返回</a>")


@app.post("/getresult")
async def getresult(re_item: ResultModel):
    re_item_dict = re_item.dict()
    html_content = cookfood.CookFood(re_item_dict['name'])
    return HTMLResponse(content=html_content)


if __name__ == '__main__':
    print_INFO("尝试启动")
    print("*" * 100)
    print("blog https://sboxm.github.io")
    print("*" * 100)
    print_INFO("获取使用提示请访问 https://github.com/cnhkbbs/zfspider")
    uvicorn.run(app)
