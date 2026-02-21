import os
import requests

def get_weather(location, key):
    url = f"https://devapi.qweather.com/v7/weather/3d?location={location}&key={key}"
    try:
        res = requests.get(url)
        # 暴力截取前 30 个字符，看看它到底回了什么鬼东西
        raw_text = res.text[:30]
        return f"状态码{res.status_code}:{raw_text}", "未知"
    except Exception as e:
        return "代码内部错误", "未知"

def main():
    app_id = os.environ.get("APP_ID")
    app_secret = os.environ.get("APP_SECRET")
    open_id = os.environ.get("OPEN_ID")
    template_id = os.environ.get("TEMPLATE_ID")
    qweather_key = os.environ.get("QWEATHER_KEY")

    vie_weather, vie_temp = get_weather("16.37,48.20", qweather_key)
    hz_weather, hz_temp = get_weather("101210101", qweather_key)

    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    access_token = requests.get(token_url).json().get("access_token")
    if not access_token:
        return

    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
    payload = {
        "touser": open_id,
        "template_id": template_id,
        "data": {
            "vie_weather": {"value": vie_weather, "color": "#173177"},
            "vie_temp": {"value": vie_temp, "color": "#173177"},
            "hz_weather": {"value": hz_weather, "color": "#173177"},
            "hz_temp": {"value": hz_temp, "color": "#173177"}
        }
    }
    requests.post(send_url, json=payload)

if __name__ == "__main__":
    main()
