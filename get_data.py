import requests
from get_cookie import GetCookie
import process_html


class GetData:

    def __init__(self, url):
        self.url = url
        self.cookie = GetCookie().get_cookie()
        self.question_list = []
        self.question_content = []

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
        self.question_list = process_html.get_list(response.text)
        return self.question_list

    def get_question(self):
        for question in self.question_list:
            response = self.session.get(question['题目链接'], cookies=self.cookie)
            self.question_content.append(process_html.get_pieces_question(response.text))
        return self.question_content

    def __del__(self):
        pass
