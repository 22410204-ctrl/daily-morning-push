import os
import requests

def get_weather(location, key):
    # 调用和风天气 3天预报接口
    url = f"https://devapi.qweather.com/v7/weather/3d?location={location}&key={key}"
    response = requests.get(url).json()
    if response.get("code") == "200":
        daily = response["daily"][0] # 获取今天的数据
        weather = daily["textDay"]
        temp = f"{daily['tempMin']}~{daily['tempMax']}度"
        return weather, temp
    return "未知", "未知"

def main():
    # 1. 获取环境变量（我们刚才填的 Secrets）
    app_id = os.environ.get("APP_ID")
    app_secret = os.environ.get("APP_SECRET")
    open_id = os.environ.get("OPEN_ID")
    template_id = os.environ.get("TEMPLATE_ID")
    qweather_key = os.environ.get("QWEATHER_KEY")

    # 2. 获取天气
    # 维也纳使用经纬度 16.37(经度),48.20(纬度)
    vie_weather, vie_temp = get_weather("16.37,48.20", qweather_key)
    # 杭州使用城市代码 101210101
    hz_weather, hz_temp = get_weather("101210101", qweather_key)

    # 3. 获取微信 Access Token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    token_res = requests.get(token_url).json()
    access_token = token_res.get("access_token")
    if not access_token:
        print("获取微信Token失败！请检查 APP_ID 和 APP_SECRET")
        return

    # 4. 组装并发送消息
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
    
    send_res = requests.post(send_url, json=payload).json()
    if send_res.get("errcode") == 0:
        print("早安推送成功！")
    else:
        print(f"推送失败，错误信息：{send_res}")

if __name__ == "__main__":
    main()
