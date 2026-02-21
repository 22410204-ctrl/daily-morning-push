import os
import requests

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

def main():
    app_id = os.environ.get("APP_ID")
    app_secret = os.environ.get("APP_SECRET")
    # 这里获取到的是 "你的ID,朋友的ID" 这样的字符串
    open_id_str = os.environ.get("OPEN_ID") 
    template_id = os.environ.get("TEMPLATE_ID")
    qweather_key = os.environ.get("QWEATHER_KEY")

    # 获取天气和空气质量
    vie_weather, vie_temp = get_weather("16.37,48.20", qweather_key)
    hz_weather, hz_temp = get_weather("101210101", qweather_key)
    vie_aqi = get_aqi("48.20", "16.37", qweather_key)
    hz_aqi = get_aqi("30.28", "120.15", qweather_key)

    # 获取微信 Access Token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    access_token = requests.get(token_url).json().get("access_token")
    if not access_token:
        print("获取 Token 失败")
        return

    # 【重点在这里】把名单用逗号切开，变成一个列表
    open_ids = open_id_str.split(",")

    # 用 for 循环，给名单上的每个人挨个发消息
    for single_open_id in open_ids:
        # 清除可能不小心打进去的空格
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
                "hz_aqi": {"value": hz_aqi, "color": "#008000"}
            }
        }
        requests.post(send_url, json=payload)
        print(f"成功发送给：{single_open_id}")

if __name__ == "__main__":
    main()
