import requests
from get_data import GetData
from get_answer import GetAnswer
from get_cookie import GetCookie
from submit_data import SubmitData, submit_data, submit_pieces_data, submit_data_file

# 目标 URL
url = "https://bigdatatech.nwafu.edu.cn/assignment/index.jsp"


def get_content(json_str):
    import json
    response = json.loads(json_str)
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    get_cookies = GetCookie()
    get_data = GetData(url=url, cookie=get_cookies.get_cookie())
    get_answer = GetAnswer()
    driver = get_cookies.get_driver()
    for chapter in get_data.get_chapter_list():
        for question_list in get_data.get_question_lists(chapter['章节链接']):
            if question_list['类别'] == "程序片段编程题":
                question_content = get_data.get_pieces_question(question_list['题目链接'])
                answer = get_answer.get_pieces_answer(question_content['题目描述'], question_content['题目代码'])
                print(get_content(answer))
                submit_pieces_data(question_list['题目链接'],
                                   list(get_content(answer)), driver)
            elif question_list['类别'] == "编程题":
                question_content = get_data.get_question(question_list['题目链接'])
                answer = get_answer.get_normal_answer(question_content['题目描述'])
                print(get_content(answer))
                try:
                    submit_data(question_list['题目链接'],
                                get_content(answer), driver)
                except:
                    submit_data_file(question_list['题目链接'], get_content(answer), driver)
    driver.quit()

