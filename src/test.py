import requests
import json

# cookies = {
#     'bid': '4Xl28mUhvMg',
# }

# headers = {
#     'User-Agent': 'api-client/1 com.douban.frodo/7.48.0(256) Android/31 product/munch vendor/Xiaomi model/22021211RC brand/Redmi  rom/miui6  network/wifi  udid/06515dd14ec6346090e79fe2b11311aec24e849c  platform/mobile',
#     # 'Accept-Encoding': 'gzip',
#     'authorization': 'Bearer 570eeb09e81f1f54052cc11db85d5dfc',
#     # 'Cookie': 'bid=4Xl28mUhvMg',
# }

# response = requests.get(
#     'https://frodo.douban.com/api/v2/noviciate/mark_recommendations? \
#     count=30& \
#     start=0& \
#     kind=movie& \
#     apikey=0dad551ec0f84ed02907ff5c42e8ec70& \
#     channel=Yingyongbao_Market& \
#     udid=06515dd14ec6346090e79fe2b11311aec24e849c& \
#     os_rom=miui6& \
#     timezone=Asia/Shanghai& \
#     _sig=C19lzWmblmTDVDC49jQP1OJXmb8%3D& \
#     _ts=1723182117',
#     cookies=cookies,
#     headers=headers,
# )
with open('../response/[284] response_frodo.douban.com_mark_recommendations.json','r',encoding='utf8')as file:
    response = json.load(file)

print(len(response['subjects']))
