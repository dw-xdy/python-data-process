'''
目前可以确定的是: 所有的问题都是同一个键(key): "subjectMatterTxt":"正交调幅星座图上的点数越多，则（    ）" 

选择题的选项的键(key): "optionA", "optionB" "optionC" "optionD"
选择题的答案的键(key): "answer": "A"，"B"，"C"，"D"

判断题就无所谓什么选项了。
判断题的答案的键(key): "answer" "1"就是正确，"0"就是错误。

应用题的话，后续应该还要手动整理。

'''
# 首先完成了第一步，已经成功得到的题目的数据。
import requests
from fake_useragent import UserAgent

session = requests.Session()
# 将Cookie设置到session的headers中，之后所有请求都会自动携带
session.headers.update(
    {
        "User-Agent": UserAgent().random,
        # 1. 保留 Cookie 头
        "Cookie": "Hm_lvt_5a2a966e966e16256f6b2a11625b597b=1777699626,1777732546,1777777476; HMACCOUNT=2A0B3DB91DEC60CD; Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjY5ZDhjYzg5LTQ4ZjAtNGMwNy05ZDc3LTE1N2RjN2MxNWIxZiJ9.-Po4-AJRkrL23Bdewrrwo1XQh1krmeGlD-6LA6d_KY_xX-gR0tL9mlA0nDiPHKFUx-dzD6OMHCoMbhDdgJ8Jcg; Hm_lpvt_5a2a966e966e16256f6b2a11625b597b=1777779433",
        
        # 2. 【关键修复】添加 Authorization 头
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjY5ZDhjYzg5LTQ4ZjAtNGMwNy05ZDc3LTE1N2RjN2MxNWIxZiJ9.-Po4-AJRkrL23Bdewrrwo1XQh1krmeGlD-6LA6d_KY_xX-gR0tL9mlA0nDiPHKFUx-dzD6OMHCoMbhDdgJ8Jcg",

        # 3. 【强烈推荐】加上 Referer 头，让请求更完整
        "Referer": "https://wisdom2.prod.shangyuninfo.com/class/details/special?roomId=2049080533266354177",
    }
)

for i in range(1, 176): 
    target_url = f"https://wisdom2.prod.shangyuninfo.com/prod-api/roomUserQuestion/info/question?cardOrder={i}"
    response = session.get(url=target_url)
    response.encoding = "utf-8"
print(response.text)
