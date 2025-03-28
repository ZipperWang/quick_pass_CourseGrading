import requests
from get_data import GetData
from get_answer import GetAnswer
# 目标 URL
url = "https://bigdatatech.nwafu.edu.cn/assignment/index.jsp"


if __name__ == "__main__":
    get_data = GetData(url=url)
    get_answer = GetAnswer()
    get_data.get_question_lists()
    for question in get_data.get_question():
        print(question)
        print(get_answer.get_normal_answer(question['题目描述']))
