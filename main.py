import requests
from get_data import GetData
from get_answer import GetAnswer

# 目标 URL
url = "https://bigdatatech.nwafu.edu.cn/assignment/index.jsp"


def get_content(json_str):
    import json
    response = json.loads(json_str)
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    get_data = GetData(url=url)
    get_answer = GetAnswer()
    get_data.get_question_lists()
    for question in get_data.get_question():
        print(question["题目描述"])
        print()
        print(get_content(get_answer.get_normal_answer(question['题目描述'])))
        print()
