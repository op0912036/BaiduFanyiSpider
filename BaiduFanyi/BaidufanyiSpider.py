import requests
import execjs
import re
import json


class BaiduFanyiSpider:
    """百度翻译爬虫"""

    def __init__(self, query):
        """初始化参数"""
        self.query = query
        self.url_ret = "https://fanyi.baidu.com/v2transapi"
        self.url_lang = "https://fanyi.baidu.com/langdetect"
        self.url_data = "https://fanyi.baidu.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Cookie": "BAIDUID=A0CB0FE1DB6D18809C712B5062BBAC6F:FG=1; BIDUPSID=A0CB0FE1DB6D18809C712B5062BBAC6F; PSTM=1538210057; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1539151103,1539251833; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; locale=zh; pgv_pvi=4554512384; delPer=0; H_PS_PSSID=1438_21082_27401_26350; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1541036302,1541037057,1541040002,1541054643; PSINO=5; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1541057937; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22jp%22%2C%22text%22%3A%22%u65E5%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D"
        }
        # self.proxies = {
        #     "https": "https://202.112.237.102:3128"
        # }

    def parse_url(self, url, params=None, data=None, method='get'):
        """解析url，获取响应内容"""
        if method == 'get':
            resp = requests.get(url=url, params=params, headers=self.headers)
        else:
            resp = requests.post(url=url, data=data, headers=self.headers)

        return resp.content.decode('utf-8')

    def get_sign_and_token(self):
        """获取sign和token数据"""
        content = self.parse_url(url=self.url_data)
        gtk = re.findall(r"<script>window.bdstoken = '';window.gtk = '(.*?)';</script>", content)[0]
        token = re.findall(r"token: '(.*?)',", content)[0]

        with open("./files/fanyi.js", "r", encoding="utf-8") as file:
            js = file.read()

        js = js.replace('u = null !== i ? i : (i = window[l] || "") || "";', 'u = "%s"' % gtk)
        cxt = execjs.compile(js)
        sign = cxt.call("e", self.query)

        return sign, token

    def get_lang(self):
        """获取语言"""
        data = {
            'query': self.query
        }
        content = self.parse_url(url=self.url_lang, data=data, method='post')
        content = json.loads(content)

        return content['lan']

    def get_data(self):
        """获取数据"""
        sign, token = self.get_sign_and_token()
        lang = self.get_lang()

        data = {
            "query": self.query,
            "transtype": "translang",
            "simple_means_flag": "3",
            "sign": sign,
            "token": token,
        }

        if lang == "zh":
            data.update({
                "from": "zh",
                "to": "en",
            })
        else:
            data.update({
                "from": "en",
                "to": "zh",
            })

        return data

    def run(self):
        """核心逻辑"""
        content = self.parse_url(url=self.url_ret, data=self.get_data(), method='post')
        content = json.loads(content)
        print(content["trans_result"]["data"][0]["dst"])


if __name__ == '__main__':
    query = input(">")

    baidufanyispider = BaiduFanyiSpider(query)
    baidufanyispider.run()
