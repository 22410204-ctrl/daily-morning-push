import os
import requests

# 👇 【非常重要】把你刚才复制的 API Host 粘贴在下面引号里！
# 例如：API_HOST = "abc1234xyz.def.qweatherapi.com"
API_HOST = "nk63ywyj8d.re.qweatherapi.com"

def get_weather(location, key):
    # 这里已经换成了你的专属通道
    url = f"https://{API_HOST}/v7/weather/3d?location={location}&key={key}"
    try:
        response = requests.get(url).json()
        if str(response.get("code")) == "200":
            daily = response["daily"][0] # 获取今天的数据
            weather = daily["textDay"]
            temp = f"{daily['tempMin']}~{daily['tempMax']}度"
            return weather, temp
        return f"接口错误码:{response.get('code')}", "未知"
    except Exception as e:
        return "请求出错了", "未知"

def main():
    app_id = os.environ.get("APP_ID")
    app_secret = os.environ.get("APP_SECRET")
    open_id = os.environ.get("OPEN_ID")
    template_id = os.environ.get("TEMPLATE_ID")
    qweather_key = os.environ.get("QWEATHER_KEY")

    if API_HOST == "请替换成你的API_HOST":
        print("等一下！你忘记在代码里填入 API Host 啦！")
        return

    # 获取维也纳和杭州天气
    vie_weather, vie_temp = get_weather("16.37,48.20", qweather_key)
    hz_weather, hz_temp = get_weather("101210101", qweather_key)

    # 获取微信钥匙
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    access_token = requests.get(token_url).json().get("access_token")
    if not access_token:
        print("获取微信Token失败！")
        return

    # 发送推送
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
