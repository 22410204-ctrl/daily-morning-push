import os
import requests
import random

# 👇 【非常重要】记得填上你的 API_HOST
API_HOST = "nk63ywyj8d.re.qweatherapi.com"

def get_weather(location, key):
    url = f"https://{API_HOST}/v7/weather/3d?location={location}&key={key}"
    try:
        response = requests.get(url).json()
        if str(response.get("code")) == "200":
            daily = response["daily"][0]
            weather = daily["textDay"]
            temp = f"{daily['tempMin']}~{daily['tempMax']}度"
            return weather, temp
        return "未知", "未知"
    except:
        return "未知", "未知"

def get_aqi(lat, lon, key):
    url = f"https://{API_HOST}/airquality/v1/daily/{lat}/{lon}?key={key}"
    try:
        response = requests.get(url).json()
        if "days" in response and len(response["days"]) > 0:
            indexes = response["days"][0].get("indexes", [])
            if indexes:
                aqi_val = indexes[0].get("aqiDisplay", "")
                category_en = indexes[0].get("category", "")
                cat_map = {"Excellent": "优", "Good": "良", "Fair": "轻度污染", "Poor": "中度污染", "Very Poor": "重度污染"}
                category_cn = cat_map.get(category_en, category_en)
                return f"{aqi_val} ({category_cn})"
        return "暂无检测数据"
    except Exception as e:
        return "暂无检测数据"

def get_daily_quote():
    # 调用免费"一言"API获取随机语录 (c=h影视, c=d文学, c=k哲学)
    url = "https://v1.hitokoto.cn/?c=h&c=d&c=k"
    try:
        res = requests.get(url, timeout=5).json()
        text = res.get("hitokoto", "")
        source = res.get("from", "佚名")
        return f"{text} ——《{source}》"
    except:
        return "如果再也不能见到你，祝你早安，午安，晚安。"

def main():
    app_id = os.environ.get("APP_ID")
    app_secret = os.environ.get("APP_SECRET")
    open_id_str = os.environ.get("OPEN_ID") 
    template_id = os.environ.get("TEMPLATE_ID")
    qweather_key = os.environ.get("QWEATHER_KEY")

    # 获取天气和空气质量
    vie_weather, vie_temp = get_weather("16.37,48.20", qweather_key)
    hz_weather, hz_temp = get_weather("101210101", qweather_key)
    vie_aqi = get_aqi("48.20", "16.37", qweather_key)
    hz_aqi = get_aqi("30.28", "120.15", qweather_key)

    # =============== 破解微信截断限制 ===============
    full_quote = get_daily_quote()
    # 我们把获取到的长句子，每 18 个字切一刀，分装到三个坑位里！
    quote_part1 = full_quote[:18] 
    quote_part2 = full_quote[18:36] 
    quote_part3 = full_quote[36:54] 
    
    # 随机德语祝福盲盒
    german_blessings = [
        "Ich wünsche dir einen schönen Tag.",
        "Jeder Tag ist ein neuer Anfang.",
        "Glaube an dich selbst!",
        "Mach das Beste aus diesem Tag!",
        "Wenn du es wirklich willst, kannst du alles schaffen.",
        "Am Ende wird alles gut. Und wenn es nicht gut ist, dann ist es noch nicht das Ende.",
        "Lächle, das Leben ist schön!",
        "Du bist großartig, genau so wie du bist.",
        "Egal, was die Zukunft bringt, du wirst immer geliebt." 
    ]
    blessing_str = random.choice(german_blessings)
    # ========================================

    # 获取微信 Access Token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    access_token = requests.get(token_url).json().get("access_token")
    if not access_token:
        print("获取 Token 失败")
        return

    open_ids = open_id_str.split(",")

    for single_open_id in open_ids:
        single_open_id = single_open_id.strip() 
        if not single_open_id:
            continue
            
        send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
        payload = {
            "touser": single_open_id,
            "template_id": template_id,
            "data": {
                "vie_weather": {"value": vie_weather, "color": "#173177"},
                "vie_temp": {"value": vie_temp, "color": "#173177"},
                "vie_aqi": {"value": vie_aqi, "color": "#008000"},  
                "hz_weather": {"value": hz_weather, "color": "#173177"},
                "hz_temp": {"value": hz_temp, "color": "#173177"},
                "hz_aqi": {"value": hz_aqi, "color": "#008000"},
                "quote1": {"value": quote_part1, "color": "#FF8C00"},       
                "quote2": {"value": quote_part2, "color": "#FF8C00"},       
                "quote3": {"value": quote_part3, "color": "#FF8C00"},       
                "german_blessing": {"value": blessing_str, "color": "#FF69B4"} 
            }
        }
        requests.post(send_url, json=payload)
        print(f"成功发送给：{single_open_id}")

if __name__ == "__main__":
    main()
