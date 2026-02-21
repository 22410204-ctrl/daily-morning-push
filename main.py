import os
import requests

# 👇 【非常重要】记得换回你刚才跑通的那个 API Host！
# 例如：API_HOST = "abc1234xyz.def.qweatherapi.com"
API_HOST = "nk63ywyj8d.re.qweatherapi.com"

def get_weather(location, key):
    # 获取天气和温度
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

def get_aqi(location, key):
    # 获取空气质量 (AQI 和 类别)
    url = f"https://{API_HOST}/v7/air/now?location={location}&key={key}"
    try:
        response = requests.get(url).json()
        if str(response.get("code")) == "200":
            now = response["now"]
            return f"{now['aqi']} {now['category']}"
        return "暂无" # 海外部分城市免费接口可能不提供空气质量，做个兜底
    except:
        return "暂无"

def main():
    app_id = os.environ.get("APP_ID")
    app_secret = os.environ.get("APP_SECRET")
    open_id = os.environ.get("OPEN_ID")
    template_id = os.environ.get("TEMPLATE_ID")
    qweather_key = os.environ.get("QWEATHER_KEY")

    # 获取天气
    vie_weather, vie_temp = get_weather("16.37,48.20", qweather_key)
    hz_weather, hz_temp = get_weather("101210101", qweather_key)
    
    # 获取空气质量
    vie_aqi = get_aqi("16.37,48.20", qweather_key)
    hz_aqi = get_aqi("101210101", qweather_key)

    # 地道德语祝福语：祝你度过愉快的一天~
    german_ending = "Ich wünsche dir einen schönen Tag~"

    # 获取微信 Access Token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    access_token = requests.get(token_url).json().get("access_token")
    if not access_token:
        return

    # 组装并发送消息
    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
    payload = {
        "touser": open_id,
        "template_id": template_id,
        "data": {
            "vie_weather": {"value": vie_weather, "color": "#173177"},
            "vie_temp": {"value": vie_temp, "color": "#173177"},
            "vie_aqi": {"value": vie_aqi, "color": "#008000"},  # 绿色字体
            "hz_weather": {"value": hz_weather, "color": "#173177"},
            "hz_temp": {"value": hz_temp, "color": "#173177"},
            "hz_aqi": {"value": hz_aqi, "color": "#008000"},    # 绿色字体
            "ending": {"value": german_ending, "color": "#FF69B4"} # 粉色字体
        }
    }
    
    requests.post(send_url, json=payload)

if __name__ == "__main__":
    main()
