import os
import requests

def get_weather(location, key):
    # 第一步检查：如果没有读到 Key
    if not key:
        return "没读到KEY", "未知"

    url = f"https://devapi.qweather.com/v7/weather/3d?location={location}&key={key}"
    try:
        res = requests.get(url)
        data = res.json()
        
        # 正常返回了200
        if str(data.get("code")) == "200":
            daily = data["daily"][0]
            weather = daily["textDay"]
            temp = f"{daily['tempMin']}~{daily['tempMax']}度"
            return weather, temp
            
        # 和风天气报错 (例如返回 401 权限错误等)
        if "error" in data:
            return f"被拒:{data['error'].get('code')}", "未知"
            
        return f"未知错:{str(data.get('code'))}", "未知"
    except Exception as e:
        return "请求出错了", "未知"

def main():
    app_id = os.environ.get("APP_ID")
    app_secret = os.environ.get("APP_SECRET")
    open_id = os.environ.get("OPEN_ID")
    template_id = os.environ.get("TEMPLATE_ID")
    qweather_key = os.environ.get("QWEATHER_KEY")

    # 获取天气
    vie_weather, vie_temp = get_weather("16.37,48.20", qweather_key)
    hz_weather, hz_temp = get_weather("101210101", qweather_key)

    # 获取微信 Access Token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    token_res = requests.get(token_url).json()
    access_token = token_res.get("access_token")
    if not access_token:
        print("获取微信Token失败！")
        return

    # 组装并发送消息
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
