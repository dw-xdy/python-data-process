# 首先完成了第一步，已经成功得到的题目的数据。
import requests
from fake_useragent import UserAgent

session = requests.Session()
# 将Cookie设置到session的headers中，之后所有请求都会自动携带
session.headers.update(
    {
        "User-Agent": UserAgent().random,
        # 1. 保留 Cookie 头
        "Cookie": "Hm_lvt_5a2a966e966e16256f6b2a11625b597b=1777699626,1777732546; HMACCOUNT=2A0B3DB91DEC60CD; Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6ImQ0NzQ0YzBkLWU1Y2QtNDk5Yi05YjJhLWI3YWY4NDg4YWJkMCJ9.swGIOpDcxGYvpVc143JCdiXs2ZvqeDDuT41oOTJo6LdbN17HkneXm5dQ7ld_vyjegzdFnCjBMbHDpbaTopA2AQ; Hm_lpvt_5a2a966e966e16256f6b2a11625b597b=1777735066; sidebarStatus=0",
        
        # 2. 【关键修复】添加 Authorization 头
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6ImQ0NzQ0YzBkLWU1Y2QtNDk5Yi05YjJhLWI3YWY4NDg4YWJkMCJ9.swGIOpDcxGYvpVc143JCdiXs2ZvqeDDuT41oOTJo6LdbN17HkneXm5dQ7ld_vyjegzdFnCjBMbHDpbaTopA2AQ",
        
        # 3. 【强烈推荐】加上 Referer 头，让请求更完整
        "Referer": "https://wisdom2.prod.shangyuninfo.com/class/details/special?roomId=2049080533266354177",
    }
)

target_url = "https://wisdom2.prod.shangyuninfo.com/prod-api/roomUserQuestion/info/question?cardOrder=1"
response = session.get(url=target_url)
response.encoding = "utf-8"
print(response.text)
