import requests

from Config import config
from get_cookie import GetCookie
import process_html


class GetData:

    def __init__(self, url):
        self.url = url
        self.cookie = GetCookie().get_cookie()
        self.chapter_list = []
        self.question_list = []
        self.question_content = []

        # 伪装成浏览器的请求头
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/134.0.0.0 Safari/537.36"
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_chapter_list(self):
        response = self.session.get(config['url']['question_list'], cookies=self.cookie)
        self.chapter_list = process_html.get_chapter(response.text)
        return self.chapter_list

    def get_question_lists(self, url):
        response = self.session.get(url, cookies=self.cookie)
        self.question_list = process_html.get_list(response.text)
        return self.question_list

    def get_question(self, url):
        response = self.session.get(url, cookies=self.cookie)
        real_data = process_html.get_question(response.text)
        self.question_content.append(real_data)
        return real_data

    def get_pieces_question(self, url):
        response = self.session.get(url, cookies=self.cookie)
        real_data = process_html.get_pieces_question(response.text)
        self.question_content.append(real_data)
        return real_data

    def __del__(self):
        pass


if __name__ == "__main__":
    GetData("https://bigdatatech.nwafu.edu.cn/includes/redirect.jsp?tab=-2").get_chapter()
