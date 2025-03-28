from bs4 import BeautifulSoup
from Config import config


def get_list(html_content:str):
    # # 读取 HTML 文件
    # with open("output.txt", "r", encoding="utf-8") as file:
    #     html_content = file.read()

    # 解析 HTML
    soup = BeautifulSoup(html_content, "lxml")

    # 存储题目信息
    questions_data = []

    # 遍历所有题目类别
    for category in soup.find_all("div", class_="add-style-title btn-secondary"):
        category_name = category.find("b").text.strip()  # 获取题目类别名称

        # 找到该类别下的表格
        table = category.find_next("table")
        if table:
            for row in table.find_all("tr")[1:]:  # 跳过表头
                cols = row.find_all("td")

                if len(cols) >= 3:
                    title_link = cols[0].find("a")  # 题目链接
                    detail_link = cols[-1].find("a", string="详细")  # 详细页面的链接

                    # 确保获取的链接存在
                    if title_link:
                        title = title_link.text.strip()
                        question_url = config['base_url'] + title_link["href"]

                        # 详细页面的链接应该从 "详细" 按钮的 href 中获取
                        detail_url = ""
                        if detail_link and detail_link.has_attr("href"):
                            detail_url = config['base_url'] + detail_link["href"]

                        # 存储题目信息
                        questions_data.append({
                            "类别": category_name,
                            "题目": title,
                            "题目链接": question_url,
                            "详细链接": detail_url
                        })

    # # 转换为 DataFrame 便于查看
    # df_questions = pd.DataFrame(questions_data)
    #
    # # 打印提取的题目信息
    # print(df_questions)
    #
    # # 可选：保存到 CSV 文件
    # df_questions.to_csv("parsed_questions.csv", index=False, encoding="utf-8")

    return questions_data


def get_question(html_content:str):
    # 读取 HTML 文件内容
    # file_path = "output_question.txt"
    # with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
    #     content = file.read()

    # 解析 HTML 内容
    soup = BeautifulSoup(html_content, "html.parser")

    # 提取题目标题
    title_tag = soup.find("h4", class_="cgcode_css-tt3ivf-Title")
    title = title_tag.get_text(strip=True) if title_tag else "未知标题"

    # 提取题目描述
    description_tag = soup.find("div", class_="cgProblemContentClass")
    description = description_tag.get_text("\n", strip=True) if description_tag else "无描述"

    return {
        "题目标题": title,
        "题目描述": description
    }


def get_pieces_question(html_content:str):
    # # 读取 HTML 文件内容
    # file_path = "output_question.txt"
    # with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
    #     content = file.read()

    # 解析 HTML 内容
    soup = BeautifulSoup(html_content, "html.parser")

    # 提取题目标题
    title_tag = soup.find("h4", class_="cgcode_css-tt3ivf-Title")
    title = title_tag.get_text(strip=True) if title_tag else "未知标题"

    # 提取题目描述
    description_tag = soup.find("div", class_="cgProblemContentClass")
    description = description_tag.get_text("\n", strip=True) if description_tag else "无描述"

    # 查找所有 <code> 标签内的 Python 代码
    code_blocks = soup.find_all("code", class_="cgcode python")

    # 提取代码文本并拼接
    python_code = "\n".join(block.get_text("\n", strip=True) for block in code_blocks)

    return {
        "题目标题": title,
        "题目描述": description,
        "题目代码": python_code
    }


if __name__ == "__main__":
    # 读取 HTML 文件内容
    file_path = "output_question.txt"
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
    get_pieces_question(content)
