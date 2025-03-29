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
    for chapter in get_data.get_chapter_list():
        for question_list in get_data.get_question_lists(chapter['章节链接']):
            for question in get_data.get_question(question_list['题目链接']):
                print()
                if question_list['类别'] == "程序片段编程题":
                    print(get_content(get_answer.get_pieces_answer(question['题目描述'], question['题目代码'])))
                elif question_list['类别'] == "编程题":
                    print(get_content(get_answer.get_normal_answer(question['题目描述'])))
                print()
