# zfspider
正方教务成绩爬虫
![140.jpg](https://cdnjson.com/images/2023/07/18/140.jpg)
# 使用
## 文件结构
```
server.py 主程序（FastAPI服务端）
spider.py 爬虫主程序(返回未处理的网页，并保存为 用户名+.text)
cookfood.py 结果整理程序(返回处理完成的html字符串，以供服务端调用)
```
## 步骤
- 设置spider.py的配置项
```
gnmkdm = 'N123456'    gnmkdm值
host_list = ['http://127.0.0.1', 'http://127.0.0.1']  教务网服务器地址
```
- 运行server.py
- 浏览器访问 http://127.0.0.1:8000/
- 提交查询任务（提交后需花费数十秒的时间执行任务）
- 获取结果（填写正确的账号获取结果）
## 参数介绍
```
账号——学号
密码——教务密码 （请确保密码与账号相匹配，错误的账号密码不会有任何提示）
姓名——中文姓名（用于登录校验）
Header——爬虫请求头(避免反爬拦截)
host——教务网服务器
```
