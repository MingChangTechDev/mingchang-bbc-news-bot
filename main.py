import os
import requests
import xml.etree.ElementTree as ET

# 從 GitHub 設定中讀取臉書金鑰
ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
PAGE_ID = os.environ.get("FB_PAGE_ID")

# 抓取 BBC 新聞
rss_url = "https://feeds.bbci.co.uk/tradchinese/rss.xml"

message = ""
try:
    response = requests.get(rss_url, timeout=30)
    root = ET.fromstring(response.content)
    item = root.find('./channel/item')
    if item is not None:
        title = item.find('title').text
        link = item.find('link').text
        message = f"【銘昌科技】即時國際熱點：{title}\n\n詳細閱讀請點：{link}"
        print("成功抓取新聞：", title)
    else:
        print("【銘昌科技】未找到 BBC 新聞文章。")
except Exception as e:
    print(f"【銘昌科技】抓取 BBC 新聞發生錯誤：{e}")

def post_to_facebook(msg):
    """發布文章到 Facebook 粉絲專頁"""
    if not ACCESS_TOKEN or not PAGE_ID:
        raise ValueError("【銘昌科技】FB_ACCESS_TOKEN 或 FB_PAGE_ID 缺少。")

    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/feed"
    payload = {
        'message': msg,
        'access_token': ACCESS_TOKEN
    }
    
    response = requests.post(url, json=payload, timeout=30)
    print("【銘昌科技】臉書伺服器回應：", response.text)
    
    # 解析臉書回應，如果有錯誤就直接讓程式中斷報錯
    try:
        data = response.json()
        if "error" in data:
            raise Exception(f"Facebook 拒絕發文: {data['error'].get('message')}")
    except Exception as parse_err:
        if "error" in response.text:
            raise Exception(f"Facebook 拒絕發文: {response.text}")

# 執行發文動作
if message:
    post_to_facebook(message)
