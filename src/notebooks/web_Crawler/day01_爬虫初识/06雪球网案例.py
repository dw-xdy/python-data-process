"""
import requests
from fake_useragent import UserAgent

# 这里和老师有些不一样的地方我需要说明, 这个雪球网在进入开发者模式的时候会遇见 debugger JS逆向,
# 所以会暂停访问, 所以我们需要右键, 点击 never pause here (一律不在此处暂停) 然后按 F8 继续访问就可以了
target_url = 'https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol=SZ399001&period=1d'
headers = {
    "User-Agent": UserAgent().random,
    'Cookie': "xq_a_token=7ed879d430984f6ea5a546808b7b9fcd64f39eb9; xqat=7ed879d430984f6ea5a546808b7b9fcd64f39eb9; xq_r_token=ef2ca2a5140cc8bab4810c2509fdec718b6f63a5; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTc2ODA5NDE1NSwiY3RtIjoxNzY2NjU2NjUxMTUyLCJjaWQiOiJkOWQwbjRBWnVwIn0.VyM80eZKEkg584_PQ7vrjDTI1zic4sWM7fuiajNo23BlzfzS7nQLaStmsaBU-Wyn7AzCbGeSAovbgThLe7SbmiOyxBtwOWn1oIxrHK5KaBGZA6CffIkT5_n-wMuUXpZRyG16noqD5b64s1CxPzwV-qg2J9vou8zasefmr2ayHrjmpdJsukwag-izCxVnYZcFYqx-kkt81bnJY8tPeMbZVQE7HmJfU609sRD5qIFly6TiGWFasc4s8hswxSY7OPwdPXMfp4qgzzswaGILQKXval0fYLRwJpKvnH_RezUD_th9m9J0PPHXDmSHCfJz7ZWhoyx0-0MIVoH17MMsR3uotg; cookiesu=161766656709540; u=161766656709540; device_id=9f3c171b22c611430ba988bb6d54a79a; Hm_lvt_1db88642e346389874251b5a1eded6e3=1766656712; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1766656712; HMACCOUNT=38BA9AD3148C45EB; smidV2=2025122517583125a544509f346ffd586cc833923f64a700ede92b96b533150; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=somw/+N1LkZP2XcNIFuwoga7F92tQIhjmGSgCoguNa8px4RT+2amqB5qAcGGybun56pXP5FnkHB51f+Z/+wgtg%3D%3D; ssxmod_itna=1-iqmxBQKDw4cDuDUxeKYKitD28qGOctG24MDl4BtGRRDIqGQGcD8hD0pvSfKyRfYDk49BHm33UALeh3aSxGXmEDBIQD5xiAbRbAA5r5SfDpiemZ_AY_udVWDZriveYl0Eky/tU/5xAAawWsyEWepD0aDmIWNiGHpDiiDBWaD0eDPxDYDGRwDneDexDd7Sgv74GWTBb3DlIW7K241_OaDYyeDD5DAh7YjjE4DG5qQAuaD7eDEGgvYFk3hDD1NloT74G1jD0H=A647_M91L0Asb=ToMWajR3DvxDkEGoDooaYcjOEoLnDR=io1gDpAxXE4KB4qix0gsNAxPOte7DIg42bh2fo=2DZDGpDDicqPnm5AmbQG3lwbjtyPNSOX8W4=fqvQDcYK2nPoiG9QeqWIzlG74mGlqwCG5Yhxzx9iT4nGKP0dYD; ssxmod_itna2=1-iqmxBQKDw4cDuDUxeKYKitD28qGOctG24MDl4BtGRRDIqGQGcD8hD0pvSfKyRfYDk49BHm33UALeh3a3xDfbq5nMG4DLli2NLe8eODD/f0cSX3Gp128P47aGUR9pUrXp=9uH5iVSaoAk0fDu46g_GtO8A6xsd6LmOX5tTK9Q0fernAZlkbq8wbeuR3VzM4daL4N50YnFZb49_i8tmb4zDX45wRKWT9qnZDU_BD0zB95_jx2lMBK=8=doewqcOj5UY4XUBx04SbsFQtq/x=wNCGxtWRd3A7I/t4d=wY4DL6LQuD2YSR5_/6x0LXrDccAa6P36=UlvMB=E=IUi5cQAuj5OnQ2CocPx0lA7ZIN2AQbqCEdLZIkhooOXdoRNZ2r9LoZt8i3Bid4eEKPed6dU7KBAKkhdbSqoUKtoIzr5QQ3SidLpvXhPt3qetYRpIdcdqzo7/Aw1I2CP4R=c0aM6vIUbo2pT4IxCp3eF0AYLW0SKYl/qc9K4amceEuB6vrAKGNChQLAT0nuy4fLehdDAD=yicKOFUc0v=XR/CWdd6k=na_374fMYLqP6OzPr4EjZ3W63Z1r8=DQ_o3gv07o38NMAUui0DHR2eE0DoRlGSrodZN2iDVSKPQTqnu2po_vYl8ad99aboefIDFyHhp0ALYclNEqCh0BG5pBpIlU3r3giVphvDxLPvPqDoBAyrbSX60DzGbix06gbxQIZ2DW4PC4vLYn54_G0YtDuO4aGzBqaDxD"
}

response = requests.get(url=target_url, headers=headers)

print(response.text)
"""


"""
import requests
from fake_useragent import UserAgent

# 【一】模拟请求雪球网主页获取 Cookie

headers = {
    "User-Agent": UserAgent().random,
}


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def get_cookies():
    # 定义目标地址
    tag_url = "https://xueqiu.com/"

    # 发起请求获取响应对象
    response = requests.get(url=tag_url, headers=headers)
    print(response.text)

    # 获取Cookie参数
    cookie_params = dict(response.cookies)

    # print(cookie_params)
    # {'cookiesu': '531711090956851', 'u': '531711090956851', 'xq_a_token': '01b99d82fffd2faf8b614e98a00cbb35d6c7ddcf', 'xq_id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcxMzY2MDQyOCwiY3RtIjoxNzExMDkwOTAxODEyLCJjaWQiOiJkOWQwbjRBWnVwIn0.l_DjE-AuBBfHd9jusczif8BDef5ApTqEY3k1HQlZuG4GchCnNoegnoltyKERKzXOz3rMYggOamBc2g5M3kvM8tDvnfixHXatCrVaq0h8sygh3rqzGraoaPaCT5tFoalGOldhNzBdViXBjWQi7zKJvHj8B7Qdl-vtnjCnAUtKtr989lMbpjMLs0_XrVbx6a-PiLHn9X37pgdya-UQ3sTT0mRYeOv1q7StVRh_tGU829SIFlKvyYWRRmU4bo3KOutN2sdxixpr_w-GMEvSSQHWG26R7uGSVOGbWP0MSB4QRTEY6VoVSHdaoYPpsHZvRlexA9ZQ4kvzhOACHHAkQE033A', 'xq_r_token': '7fe9b3213c399b15eee3c5bca4841433a03128a6', 'xqat': '01b99d82fffd2faf8b614e98a00cbb35d6c7ddcf', 'acw_tc': '2760826617110909568441159ed1c3d4d3756a8dcb29b019731e2f7b1878e1'}
    return cookie_params


def get_data():
    # 【一】获取 cookies 参数
    cookie_params = get_cookies()
    # 【二】定义目标网址
    tag_url = "https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=SH000001,SZ399001,SZ399006,SH000688,SH000016,SH000300,BJ899050,HKHSI,HKHSCEI,HKHSTECH,.DJI,.IXIC,.INX"
    # 【三】携带 Cookie 获取指定数据
    # response = requests.get(url=tag_url, headers=headers)
    # （1）当我们不携带 cookies 时，返回的数据是
    # {'error_description': '遇到错误，请刷新页面或者重新登录帐号后再试', 'error_uri': '/v5/stock/batch/quote.json', 'error_data': None, 'error_code': '400016'}

    # （2）携带 cookie  请求数据
    response = requests.get(url=tag_url, headers=headers, cookies=cookie_params)
    # [1] json 格式的数据
    # data_json = response.json()
    # print(data_json)
    # [2] 二进制格式的数据
    data_bytes = response.content
    # 对二进制数据进行解码
    data_bytes = data_bytes.decode('utf-8')
    print(data_bytes)


print(get_cookies())
"""


# session 对象 ---> 可以帮助我们存储 Cookie 信息 发送求
# 导入 requests 模块
import requests

# 导入伪装UA请求头
from fake_useragent import UserAgent

# 定义请求头
headers = {
    "User-Agent": UserAgent().random,
}

# 创建 session 对象 (使用session访问网址)
session = requests.Session()


def get_data():
    # 定义目标地址
    tag_url = "https://xueqiu.com/"

    # 发起请求获取响应对象
    session.get(
        url=tag_url, headers=headers
    )  # 发起请求获取到的Cookie信息回自动存储到 session 对象中

    # 【二】定义目标网址
    tag_url = "https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol=SZ399001&period=1d"
    # 【三】不用手动携带 cookie 即可获取指定的数据
    response = session.get(url=tag_url, headers=headers)

    # [1] json 格式的数据
    # data_json = response.json()
    # print(data_json)
    # [2] 二进制格式的数据
    data_bytes = response.content
    # 对二进制数据进行解码
    data_bytes = data_bytes.decode("utf-8")
    print(data_bytes)


get_data()
