import requests
from get_data import GetData
# 目标 URL
url = "https://bigdatatech.nwafu.edu.cn/assignment/index.jsp"


if __name__ == "__main__":
    GetData(url=url).get_question()