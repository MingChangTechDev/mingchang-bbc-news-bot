import os
import requests

# 自動查詢粉專與 IG ID 的小幫手
token = os.environ.get('FB_ACCESS_TOKEN')
if token:
    url = f'https://graph.facebook.com/v18.0/me/accounts?fields=name,id,instagram_business_account&access_token={token}'
    response = requests.get(url).json()
    print('========================================')
    print('【機器人幫你查到的粉專與 IG ID 如下】')
    print(response)
    print('========================================')
else:
    print('找不到 FB_ACCESS_TOKEN，請檢查 Secrets 設定。')
