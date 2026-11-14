import os
import urllib.request
import xml.etree.ElementTree as ET
import json
import urllib.parse

# 1. 抓取 BBC 科技與國際最新新聞 RSS
def get_bbc_news():
    url = "http://feeds.bbci.co.uk/news/technology/rss.xml"
    req = urllib.request.urlopen(url)
    xml_data = req.read()
    root = ET.fromstring(xml_data)
    item = root.find("./channel/item")
    title = item.find("title").text
    description = item.find("description").text
    link = item.find("link").text
    return title, description, link

# 2. 透過 Gemini AI 轉化成「科技帶來溫暖、給人希望與好心情」的繁體中文貼文
def generate_warm_post(title, description, link):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "12345":
        return f"【科技暖心快訊】{title}\n\n{description}\n\n用科技帶來溫暖與希望，祝大家今天心情愉快！\n—— 銘昌科技開發有限公司 暖心分享"

    prompt = (
        f"你現在是「銘昌科技開發有限公司」的暖心品牌大使。請根據以下這則 BBC 科技新聞，"
        f"用繁體中文寫一篇約 150~200 字的社群貼文。\n"
        f"核心要求：現在市場環境較冷清、大家生活壓力大，請過濾掉過度沉重或負面的情緒，"
        f"強調「科技帶來的溫暖、對未來的希望、生活會越來越好」，語氣真誠、正向、讓人讀了心情愉快。\n"
        f"文末請務必加上固定署名：\n—— 銘昌科技開發有限公司 暖心分享\n\n"
        f"新聞標題：{title}\n新聞摘要：{description}"
    )
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req) as res:
        result = json.loads(res.read().decode("utf-8"))
        return result["candidates"][0]["content"]["parts"][0]["text"]

# 3. 自動發佈到 Facebook 粉絲專頁
def post_to_facebook(message):
    page_id = os.environ.get("FB_PAGE_ID")
    token = os.environ.get("FB_ACCESS_TOKEN")
    if not page_id or not token or token == "12345":
        print("尚未設定 FB 金鑰，跳過 FB 發佈。")
        return
    url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
    data = urllib.parse.urlencode({"message": message, "access_token": token}).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req) as res:
        print("FB 發佈成功：", res.read().decode("utf-8"))

# 4. 自動發佈到 Instagram（搭配科技希望主題圖）
def post_to_instagram(message):
    ig_id = os.environ.get("IG_USER_ID")
    token = os.environ.get("FB_ACCESS_TOKEN")
    if not ig_id or not token or ig_id == "12345" or token == "12345":
        print("尚未設定 IG 金鑰，跳過 IG 發佈。")
        return
    # 使用固定高品質科技溫暖意象圖作為 IG 封面
    image_url = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1080&q=80"
    create_url = f"https://graph.facebook.com/v19.0/{ig_id}/media"
    create_data = urllib.parse.urlencode({
        "image_url": image_url,
        "caption": message,
        "access_token": token
    }).encode("utf-8")
    req1 = urllib.request.Request(create_url, data=create_data)
    with urllib.request.urlopen(req1) as res1:
        creation_id = json.loads(res1.read().decode("utf-8"))["id"]

    pub_url = f"https://graph.facebook.com/v19.0/{ig_id}/media_publish"
    pub_data = urllib.parse.urlencode({
        "creation_id": creation_id,
        "access_token": token
    }).encode("utf-8")
    req2 = urllib.request.Request(pub_url, data=pub_data)
    with urllib.request.urlopen(req2) as res2:
        print("IG 發佈成功：", res2.read().decode("utf-8"))

if __name__ == "__main__":
    title, desc, link = get_bbc_news()
    warm_message = generate_warm_post(title, desc, link)
    print("生成的暖心貼文：\n", warm_message)
    post_to_facebook(warm_message)
    post_to_instagram(warm_message)
