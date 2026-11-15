import requests
import feedparser
import xml.etree.ElementTree as ET

# 抓取 BBC 新聞並發布到粉絲專頁
rss_url = "https://feeds.bbci.co.uk/tradchinese/rss.xml"

try:
    response = requests.get(rss_url, timeout=30)
    root = ET.fromstring(response.content)
    item = root.find('./channel/item')
    if item is not None:
        title = item.find('title').text
        link = item.find('link').text
        message = f"【銘昌科技】即時國際熱點：{title}\n\n詳細閱讀請點：{link}"
    else:
        print("【銘昌科技】未找到 BBC 新聞文章。")
except Exception as e:
    print(f"【銘昌科技】抓取 BBC 新聞發生錯誤：{e}")

# 預備發文文案
# message = "【銘昌科技】推薦優質全球 AI 科技趨勢與動態，為您帶來智慧產業新氣象！"

def post_to_facebook(message):
    """發布文章到 Facebook 粉絲專頁"""
    if not ACCESS_TOKEN or not PAGE_ID:
        print("【銘昌科技】FB_ACCESS_TOKEN 或 FB_PAGE_ID 缺少，跳過發文。")
        return

    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/feed"
    payload = {
        'message': message,
        'access_token': ACCESS_TOKEN
    }
    
    response = requests.post(url, json=payload, timeout=30)
    print("【銘昌科技】發文結果：", response.text)
