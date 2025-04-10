import json
import os

from openai import OpenAI
from Config import config


class GetAnswerByCache:
    def __init__(self):
        self.answers = {}
        self.null = True
        if not os.path.exists('answers_cache.json'):
            open('answers_cache.json', 'w', encoding='utf-8')
            self.null = True

    def update_answer(self, name, answer):
        if not self.null:
            return ""
        self.answers[name] = answer
        with open('answers_cache.json', 'w', encoding='utf-8') as f:
            json.dump(self.answers, f, ensure_ascii=False, indent=4)

    def find_answer(self, name):
        if not self.null:
            return ""
        with open('answers_cache.json', 'r', encoding='utf-8') as f:
            file_content = f.read().strip()
            if file_content:
                self.answers = json.loads(file_content)
        if name in self.answers:
            return self.answers[name]
        else:
            return ""


class GetAnswer(GetAnswerByCache):
    def __init__(self):
        super().__init__()
        self.client = OpenAI(
            api_key=config['model_key'],
            base_url=config['model_url'],
        )

    # def get_pieces_answer(self, question: str, code: str):
    #     completion = self.client.chat.completions.create(
    #         model=config['model_name'],
    #         messages=[
    #             {'role': 'system',
    #              'content': "现在你是一名Python初学者，你需要解决一道程序片段编程题。"
    #                         "要求:input函数参数必须为空，严格按照题目例子输出答案代码，以列表格式输出需要填的空的答案，你只需要找出题目的空并输出答案就可以.不要包含```python"
    #                         "例如['答案1','答案2']"
    #                         "使用utf-8编码"},
    #             {'role': 'user', 'content': question + code}],
    #     )
    #     return completion.model_dump_json()
    #
    # def get_normal_answer(self, question: str):
    #     completion = self.client.chat.completions.create(
    #         model=config['model_name'],
    #         messages=[
    #             {'role': 'system',
    #              'content': "现在你是一名Python初学者，你需要解决一道编程题。"
    #                         "要求:input函数参数必须为空，严格按照题目例子输出答案代码，你只需要输出答案就可以.不要包含```python"
    #                         "例如: print('hello world')"
    #                         "使用utf-8编码"},
    #             {'role': 'user', 'content': question}],
    #     )
    #     return completion.model_dump_json()

    def get_pieces_answer(self, question: str, code: str):
        answer = super().find_answer(question)
        if not answer == "":
            return answer

        reasoning_content = ""  # 定义完整思考过程
        answer_content = ""  # 定义完整回复
        is_answering = False  # 判断是否结束思考过程并开始回复

        # 创建聊天完成请求
        completion = self.client.chat.completions.create(
            model=config['model_name'],  # 此处以 qvq-max 为例，可按需更换模型名称
            messages=[
                {
                    "role": "system",
                    "content": [{"type": "text",
                                 "text": "现在你是一名Python初学者，你需要解决一道程序片段编程题。"
                                         "要求:input函数参数必须为空，严格按照题目例子输出答案代码，"
                                         "以列表格式输出需要填的空的答案，你只需要找出题目的空并输出答案就可以.返回不包含任何MarkDown代码块的代码"
                                         "例如['答案1','答案2','答案3']"
                                         "使用utf-8编码，并注意题目有多少空"}],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question + code},
                    ],
                },
            ],
            stream=True,
        )

        for chunk in completion:
            # 如果chunk.choices为空，则打印usage
            if not chunk.choices:
                pass
            else:
                delta = chunk.choices[0].delta
                # 打印思考过程
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                    print(delta.reasoning_content, end='', flush=True)
                    reasoning_content += delta.reasoning_content
                else:
                    # 开始回复
                    if delta.content != "" and is_answering is False:
                        is_answering = True
                    answer_content += delta.content
        super().update_answer(question, answer_content)
        return answer_content

    def get_normal_answer(self, question: str):
        answer = super().find_answer(question)
        if not answer == "":
            return answer

        reasoning_content = ""  # 定义完整思考过程
        answer_content = ""  # 定义完整回复
        is_answering = False  # 判断是否结束思考过程并开始回复

        # 创建聊天完成请求
        completion = self.client.chat.completions.create(
            model=config['model_name'],  # 此处以 qvq-max 为例，可按需更换模型名称
            messages=[
                {
                    "role": "system",
                    "content": [{"type": "text",
                                 "text": "现在你是一名Python初学者，你需要解决一道编程题。"
                                         "要求:input函数参数必须为空，严格按照题目例子输出答案代码，你只需要输出答案就可以.返回不包含任何MarkDown代码块的代码"
                                         "例如: print('hello world')"
                                         "使用utf-8编码"}],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                    ],
                },
            ],
            stream=True,
        )

        for chunk in completion:
            # 如果chunk.choices为空，则打印usage
            if not chunk.choices:
                pass
            else:
                delta = chunk.choices[0].delta
                # 打印思考过程
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                    print(delta.reasoning_content, end='', flush=True)
                    reasoning_content += delta.reasoning_content
                else:
                    # 开始回复
                    if delta.content != "" and is_answering is False:
                        is_answering = True
                    answer_content += delta.content

        super().update_answer(question, answer_content)

        return answer_content

    def __del__(self):
        pass


if __name__ == "__main__":
    GetAnswer.get_pieces_answer()
