# coding:utf-8
import json
from urllib.request import urlopen


def get_country(ip_address):
    """
    根据IP地址获取国家
    :param ip_address:
    :return: country
    """
    response = urlopen("http://freegeoip.net/json/"+ip_address).read().decode('utf-8')
    response_json = json.loads(response)
    print(response_json)
    return response_json.get("country_code")

if __name__ == "__main__":
    ip = "50.78.253.58"
    print(ip+"'s country is:"+get_country(ip))
