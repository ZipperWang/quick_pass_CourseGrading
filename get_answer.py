from openai import OpenAI
from Config import config
from get_data import GetData


class GetAnswer:
    def __init__(self):
        self.client = OpenAI(
            api_key=config['model_key'],
            base_url=config['model_url'],
        )

    def get_pieces_answer(self, question: str):
        completion = self.client.chat.completions.create(
            model=config['model_name'],
            # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                {'role': 'system',
                 'content': "现在你是一名Python初学者，你需要解决一道编程题，要求:input函数参数必须为空，严格按照题目例子输出答案，若为填空题，以列表格式输出答案，你只需要输出答案就可以."
                            "例如['答案1','答案2']"},
                {'role': 'user', 'content': question}],
        )
        return completion.model_dump_json()

    def get_normal_answer(self, question: str):
        completion = self.client.chat.completions.create(
            model=config['model_name'],
            # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                {'role': 'system',
                 'content': "现在你是一名Python初学者，你需要解决一道编程题，要求:input函数参数必须为空，严格按照题目例子输出答案，若为填空题，以列表格式输出答案，你只需要输出答案就可以."
                            "例如: print('hello world')"},
                {'role': 'user', 'content': question}],
        )
        return completion.model_dump_json()

    def __del__(self):
        pass


if __name__ == "__main__":
    GetAnswer.get_pieces_answer()
