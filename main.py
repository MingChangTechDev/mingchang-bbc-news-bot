import os
import requests
import xml.etree.ElementTree as ET

# 讀取 GitHub Secrets 安全密碼箱中的授權與 ID
ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
PAGE_ID = os.environ.get('FB_PAGE_ID')
IG_USER_ID = os.environ.get('IG_USER_ID')

def fetch_latest_bbc_news():
    """自動抓取 BBC 最新國際與科技新聞"""
    rss_url = "http://feeds.bbci.co.uk/news/world/rss.xml"
    try:
        response = requests.get(rss_url)
        root = ET.fromstring(response.content)
        item = root.find('./channel/item')
        if item is not None:
            title = item.find('title').text
            link = item.find('link').text
            return f"【銘昌科技・國際前瞻動態】\n\n{title}\n\n詳細閱讀：{link}"
    except Exception as e:
        print(f"抓取 BBC 新聞發生錯誤: {e}")
    
    # 預備備用文案
    return "【銘昌科技】持續掌握全球 AI 與科技趨勢脈動，為您帶來最新專業洞察！"

def post_to_facebook(message):
    """發布貼文到 Facebook 粉絲專頁"""
    if not ACCESS_TOKEN or not PAGE_ID:
        print("未設定 FB_ACCESS_TOKEN 或 FB_PAGE_ID，略過 FB 發文。")
        return
    
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/feed"
    payload = {
        'message': message,
        'access_token': ACCESS_TOKEN
    }
    res = requests.post(url, data=payload).json()
    print("Facebook 發文結果:", res)

def post_to_instagram(message):
    """發布貼文到 Instagram 商業帳號"""
    if not ACCESS_TOKEN or not IG_USER_ID:
        print("未設定 FB_ACCESS_TOKEN 或 IG_USER_ID，略過 IG 發文。")
        return
    
    # Instagram 圖文發布需要搭配一張高畫質科技感圖片
    image_url = "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1080&q=80"
    
    # 步驟 1：建立 IG 媒體容器
    container_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media"
    container_payload = {
        'image_url': image_url,
        'caption': message,
        'access_token': ACCESS_TOKEN
    }
    container_res = requests.post(container_url, data=container_payload).json()
    print("IG 建立容器結果:", container_res)
    
    if 'id' in container_res:
        creation_id = container_res['id']
        # 步驟 2：正式發布該容器
        publish_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media_publish"
        publish_payload = {
            'creation_id': creation_id,
            'access_token': ACCESS_TOKEN
        }
        publish_res = requests.post(publish_url, data=publish_payload).json()
        print("IG 發布結果:", publish_res)

if __name__ == '__main__':
    print("開始執行銘昌科技 BBC 自動發布機器人...")
    news_text = fetch_latest_bbc_news()
    print("準備發布的內容：\n", news_text)
    
    # 同步發布至 FB 與 IG
    post_to_facebook(news_text)
    post_to_instagram(news_text)
    print("機器人執行完畢！")
