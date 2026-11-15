import os
import requests
import xml.etree.ElementTree as ET

# 銘昌科技開發有限公司 - 每日國際新聞推播系統
ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
PAGE_ID = os.environ.get("FB_PAGE_ID")

# 抓取 BBC 中文網新聞
rss_url = "https://feeds.bbci.co.uk/zhongwen/trad/rss.xml"

message = ""
try:
    response = requests.get(rss_url, timeout=10)
    root = ET.fromstring(response.content)
    item = root.find("./channel/item")
    if item is not None:
        title = item.find("title").text
        link = item.find("link").text
        message = f"【銘昌科技｜精選國際快訊】\n\n{title}\n\n閱讀完整報導：{link}\n\n— 銘昌科技開發有限公司 敬上"
    else:
        message = "【銘昌科技｜精選國際快訊】目前暫無最新報導更新。"
except Exception as e:
    print(f"抓取新聞時發生異常: {e}")

# 發送至 Facebook 粉絲專頁
if ACCESS_TOKEN and PAGE_ID and message:
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    res = requests.post(url, data=payload)
    print("發送狀態碼:", res.status_code)
    print("回應內容:", res.text)
else:
    print("缺少必要金鑰或新聞內容為空，無法發送。")
