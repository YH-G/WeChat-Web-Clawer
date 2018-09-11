import requests

headers = {
    'Cookie': 'ABTEST=0|1528309479|v1; IPLOC=CA; SUID=2E2173AE1F2D940A000000005B1826E7; SUID=2E2173AE5F20940A000000005B1826E8; weixinIndexVisited=1; SUV=000251E7AE73212E5B1826F06C90D638; SNUID=BDB5E03A9396FE69DCF7CDF594FB51C5; JSESSIONID=aaa7SwnKxxDaPgFHV4lnw; sct=2; ppinf=5|1528312525|1529522125|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo1Okdhb3lofGNydDoxMDoxNTI4MzEyNTI1fHJlZm5pY2s6NTpHYW95aHx1c2VyaWQ6NDQ6bzl0Mmx1S1JGalh0aHJVa3RaRWtjYjhzRHAyWUB3ZWl4aW4uc29odS5jb218; pprdig=uFsto1mGzmD6QnKuUyptK-sfv5pcEf0tPp_CVg_GsThkf87nKWFDcYGkG4tH8dRdwuaUvxgNU343jrAS5CGr2YTHMYI_VtRr-WSMh7C4dC06VIc2DKyimGlxzhiFOBgTr47HtGTxKm1djjVvpFYcnNuPHC5mgQpETcYI_QlNyAY; sgid=19-35406455-AVsYMs0xkIKAEnIbrHDsRx0; ppmdig=152831252700000014dbb32f9d7227c86eb2a3e44dcdf809',
    'DNT': '1',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}


ip_proxy = 'http://142.4.207.235:80'

url = 'http://weixin.sogou.com/weixin?query=%E9%A3%8E%E6%99%AF&type=2&page=1'

# url = 'http://ip.chinaz.com/getip.aspx'

# url = 'https://www.google.com'

proxies = {
    "http": ip_proxy,
    "https": ip_proxy,
}
response = requests.get(url, headers=headers, proxies=proxies)

print(response.status_code)
# print(response.text)
