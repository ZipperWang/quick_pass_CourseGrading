import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import time
from Config import config
from bs4 import BeautifulSoup

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def submit_pieces_data(url, answer: list, driver):
    driver.get(url=url)
    time.sleep(2)

    # 设置答案：answer1、answer2、answer3
    driver.find_element(By.NAME, "answer1").clear()
    driver.find_element(By.NAME, "answer1").send_keys(answer[0])

    driver.find_element(By.NAME, "answer2").clear()
    driver.find_element(By.NAME, "answer2").send_keys(answer[1])

    driver.find_element(By.NAME, "answer3").clear()
    driver.find_element(By.NAME, "answer3").send_keys(answer[2])
    # count = 1
    # for e in answer:
    #     driver.find_element(By.NAME, f"answer{count}").clear()
    #     driver.find_element(By.NAME, f"answer{count}").send_keys(e)
    #     count += 1

    # 点击“提交”按钮
    submit_btn = driver.find_element(By.ID, "cgSubmitBtn")
    submit_btn.click()

    # 等待结果 iframe 加载（可加判断）
    time.sleep(5)

    # 可选：抓取 iframe 内容（显示结果）
    driver.switch_to.frame("showmessageFRAME")

    # 等待 iframe 中某个特定元素加载（比如 div、表格等）
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        # 获取结果 HTML
        result_html = driver.page_source
    except Exception as e:
        result_html = ""
        print("结果加载失败:", e)

    # 假设 result_html 是你通过 Selenium 拿到的 iframe HTML
    soup = BeautifulSoup(result_html, "html.parser")

    # 提取得分
    score_tag = soup.find("div", id="result").find_all("p")[1]
    score = score_tag.text.replace("得分：", "").strip()

    # 提取测试数据行
    table_rows = soup.select("div#result table tr")[1:]  # 跳过表头行
    results = []
    for row in table_rows:
        cols = row.find_all("td")
        if len(cols) == 2:
            test_case = cols[0].text.strip()
            verdict = cols[1].text.strip()
            results.append((test_case, verdict))

    # 输出结果
    print("得分：", score)
    for case, verdict in results:
        print(f"{case} → {verdict}")


def submit_data(url, answer, driver):
    driver.get(url=url)
    time.sleep(2)

    # 设置答案：answer1、answer2、answer3
    driver.execute_script(f'''
        const editor = document.querySelector('.CodeMirror').CodeMirror;
        editor.setValue(`{answer}`);
    ''')

    # 点击“提交”按钮
    submit_btn = driver.find_element(By.ID, "cgSubmitBtn")
    submit_btn.click()

    # 等待结果 iframe 加载（可加判断）
    time.sleep(5)

    # 可选：抓取 iframe 内容（显示结果）
    driver.switch_to.frame("showmessageFRAME")

    # 等待 iframe 中某个特定元素加载（比如 div、表格等）
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        # 获取结果 HTML
        result_html = driver.page_source
    except Exception as e:
        result_html = ""
        print("结果加载失败:", e)

    # 假设 result_html 是你通过 Selenium 拿到的 iframe HTML
    soup = BeautifulSoup(result_html, "html.parser")

    # 提取得分
    score_tag = soup.find("div", id="result").find_all("p")[1]
    score = score_tag.text.replace("得分：", "").strip()

    # 提取测试数据行
    table_rows = soup.select("div#result table tr")[1:]  # 跳过表头行
    results = []
    for row in table_rows:
        cols = row.find_all("td")
        if len(cols) == 2:
            test_case = cols[0].text.strip()
            verdict = cols[1].text.strip()
            results.append((test_case, verdict))

    # 输出结果
    print("得分：", score)
    for case, verdict in results:
        print(f"{case} → {verdict}")


def submit_data_file(url, answer: str, driver):
    # 再打开题目页
    driver.get(url)
    time.sleep(2)

    with open("answer.py", "w", encoding="utf-8") as file:
        file.write(answer)

    upload_input = driver.find_element(By.ID, "CGFILE")
    upload_input.send_keys(os.path.abspath("answer.py"))

    # ==== 提交 ====
    submit_btn = driver.find_element(By.ID, "cgSubmitBtn")
    submit_btn.click()

    # ==== 切换 iframe 并等待结果 ====
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "showmessageFrame")))
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "result")))

    # ==== 提取判题结果 ====
    soup = BeautifulSoup(driver.page_source, "html.parser")

    score = soup.find("p", string=lambda t: t and "得分" in t)
    score = score.text.replace("得分：", "").strip() if score else "未知"

    rows = soup.select("div#result table tr")[1:]
    results = []
    for row in rows:
        tds = row.find_all("td")
        if len(tds) == 2:
            test_case = tds[0].text.strip()
            verdict = tds[1].text.strip()
            results.append((test_case, verdict))

    # ==== 输出结果 ====
    print(f"得分：{score}")
    for case, verdict in results:
        print(f"{case} → {verdict}")


class SubmitData:
    def __init__(self):
        pass

    def __del__(self):
        pass
