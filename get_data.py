import requests

from get_cookie import GetCookie

# 目标 URL
class GetData:

    def __init__(self, url):
        self.url = url
        #url = "https://bigdatatech.nwafu.edu.cn/assignment/index.jsp"
        # self.cookies = {'Hm_lpvt_9eca16a516f8b449709378fbcbb6b200': '1743068189',
        #            'Hm_lvt_9eca16a516f8b449709378fbcbb6b200': '1743068185',
        #            'HMACCOUNT': '174D9D8C3790FB00',
        #            'JSESSIONID': '4BB48F640946DCF510B1BC4FA0103BF7'}

        self.cookie = GetCookie().get_cookie()


        # 伪装成浏览器的请求头
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Referer": "https://bigdatatech.nwafu.edu.cn/",
            "Sec-Ch-Ua": '"Chromium";v="134", "Not-A-Brand";v="24", "Microsoft Edge";v="134"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)
    def get_question_lists(self):
        response = self.session.get(self.url, cookies=self.cookie)
        print(response.status_code)
        print(response.text)
        # 打开文件并写入
        with open("output.txt", "w", encoding="utf-8") as file:
            print(response.text, file=file)
        return

    def get_question(self):
        response = self.session.get("https://bigdatatech.nwafu.edu.cn/assignment/programFillGapList.jsp?proNum=1&assignID=1287", cookies=self.cookie)
        print(response.text)
        with open("output_question.txt", "w", encoding="utf-8") as file:
            print(response.text, file=file)
        return

    def __del__(self):
        pass
