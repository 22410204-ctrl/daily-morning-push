import os
import requests

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
    # 根据你提供的文档，空气质量使用的是 纬度/经度 的路径
    url = f"https://{API_HOST}/airquality/v1/daily/{lat}/{lon}?key={key}"
    try:
        response = requests.get(url).json()
        # 解析返回的复杂 JSON 找到 aqi 和 等级
        if "days" in response and len(response["days"]) > 0:
            indexes = response["days"][0].get("indexes", [])
            if indexes:
                aqi_val = indexes[0].get("aqiDisplay", "")
                category_en = indexes[0].get("category", "")
                
                # 把英文等级翻译成中文
                cat_map = {"Excellent": "优", "Good": "良", "Fair": "轻度污染", "Poor": "中度污染", "Very Poor": "重度污染"}
                category_cn = cat_map.get(category_en, category_en)
                
                return f"{aqi_val} ({category_cn})"
        return "暂无检测数据"
    except Exception as e:
        return "暂无检测数据"

def main():
    app_id = os.environ.get("APP_ID")
    app_secret = os.environ.get("APP_SECRET")
    open_id = os.environ.get("OPEN_ID")
    template_id = os.environ.get("TEMPLATE_ID")
    qweather_key = os.environ.get("QWEATHER_KEY")

    # 获取天气 (维也纳:16.37,48.20 | 杭州:101210101)
    vie_weather, vie_temp = get_weather("16.37,48.20", qweather_key)
    hz_weather, hz_temp = get_weather("101210101", qweather_key)
    
    # 获取空气质量 (注意顺序是 纬度/经度)
    # 维也纳 纬度:48.20 经度:16.37
    vie_aqi = get_aqi("48.20", "16.37", qweather_key)
    # 杭州 纬度:30.28 经度:120.15
    hz_aqi = get_aqi("30.28", "120.15", qweather_key)

    # 德语祝福语
    german_ending = "Ich wünsche dir einen schönen Tag~"

    # 获取微信 Access Token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    access_token = requests.get(token_url).json().get("access_token")
    if not access_token:
        return

    # 【重点在这里】把名单用逗号切开，变成一个列表
    open_ids = open_id_str.split(",")

    for single_open_id in open_ids:
        # 清除可能不小心打进去的空格
        single_open_id = single_open_id.strip() 
        if not single_open_id:
            continue
            
    # 组装并发送消息
    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
    payload = {
        "touser": open_id,
        "template_id": template_id,
        "data": {
            "vie_weather": {"value": vie_weather, "color": "#173177"},
            "vie_temp": {"value": vie_temp, "color": "#173177"},
            "vie_aqi": {"value": vie_aqi, "color": "#008000"},  
            "hz_weather": {"value": hz_weather, "color": "#173177"},
            "hz_temp": {"value": hz_temp, "color": "#173177"},
            "hz_aqi": {"value": hz_aqi, "color": "#008000"},    
            "ending": {"value": german_ending, "color": "#FF69B4"} 
        }
    }
    
    requests.post(send_url, json=payload)
    print(f"成功发送给：{single_open_id}")

if __name__ == "__main__":
    main()
