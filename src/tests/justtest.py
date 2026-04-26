import requests
from fake_useragent import UserAgent

target_url = "https://www.zaixiankaoshi.com/online/?paperId=14413735&practice=&modal=2&is_recite=&qtype=&text=%E9%9A%8F%E6%9C%BA%E7%BB%83%E4%B9%A0&sequence=0&is_collect=1&kid=101706&is_vip_paper=0&random_size=200"

headers = {


    'User-Agent': UserAgent().random
}

response = requests.get(url=target_url, headers=headers)
response.encoding = 'utf-8'
print(response.text)