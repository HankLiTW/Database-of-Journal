import csv
import requests
from bs4 import BeautifulSoup
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading

# 随机生成的十个User-Agent字符串
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Firefox/100.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1000.100 Safari/537.36'
]

# 存储链接文件和输出文件的列表
link_files = ['a1.csv']  # 添加更多链接文件
output_files = ['a_d.csv']

def process_link(link, output_file):
    try:
        # 初始化html_data为空字符串
        html_data = ""

        # 随机选择一个User-Agent
        user_agent = random.choice(user_agents)

        # 设置请求头中的User-Agent
        headers = {
            'User-Agent': user_agent
        }

        # 发送HTTP请求
        response = requests.get(link, headers=headers)

        # 检查是否成功获取网页内容
        if response.status_code == 200:
            # 使用BeautifulSoup解析网页内容
            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取Authors
            author_buttons = soup.select('.button-link-primary[data-xocs-content-type="author"]')
            authors = []
            for button in author_buttons:
                given_name_elem = button.select_one('.given-name')
                surname_elem = button.select_one('.text.surname')
                if given_name_elem and surname_elem:
                    given_name = given_name_elem.get_text()
                    surname = surname_elem.get_text()
                    authors.append(f"{given_name} {surname}")
            formatted_authors = ', '.join(authors)

            # 使用meta标签中的元数据提取信息
            citation_title = soup.find('meta', {'name': 'citation_title'})
            citation_journal_title = soup.find('meta', {'name': 'citation_journal_title'})
            citation_publication_date = soup.find('meta', {'name': 'citation_publication_date'})
            
            if citation_title:
                citation_title = citation_title['content']
            else:
                citation_title = ""

            if citation_journal_title:
                citation_journal_title = citation_journal_title['content']
            else:
                citation_journal_title = ""

            if citation_publication_date:
                citation_publication_date = citation_publication_date['content'][:4]
            else:
                citation_publication_date = ""

            # 提取JEL数据
            jel_tags = soup.select('.Keywords .keywords-section:has(h2:-soup-contains("JEL classification")) .keyword span')
            jel_data = ', '.join(tag.get_text() for tag in jel_tags)

            # 提取Keywords信息
            keywords_tags = soup.select('.Keywords .keywords-section:has(h2:-soup-contains("Keywords")) .keyword span')
            keywords = ', '.join(tag.get_text() for tag in keywords_tags)

            # 使用Selenium获取机构信息
            # 启动一个浏览器
            driver = webdriver.Chrome()

            # 打开网页
            driver.get(link)
            
            # 点击按钮，最多尝试三次
            for _ in range(3):
                try:
                    # 等待"Show more"按钮可点击
                    show_more_button = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.ID, 'show-more-btn'))
                    )
                    # 点击按钮
                    show_more_button.click()

                    # 等待页面加载完成
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'affiliation'))
                    )

                    # 获取页面源代码
                    html_data = driver.page_source

                    # 成功加载数据，退出循环
                    break
                except Exception as e:
                    print(f"Failed to load data, retrying ({e}")

            # 关闭浏览器
            driver.quit()

            # 使用BeautifulSoup解析页面内容
            soup = BeautifulSoup(html_data, 'html.parser')

            # 提取机构信息
            affiliation_tags = soup.select('.affiliation dd')
            affiliations = [tag.get_text() for tag in affiliation_tags]

            # 将机构信息用逗号分隔
            affiliations_text = ', '.join(affiliations)

            # 将提取的信息写入CSV文件
            with open(output_file, 'a', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([formatted_authors, affiliations_text, citation_publication_date, citation_journal_title, citation_title, jel_data, keywords])
                print(f"Successfully processed link: {link}")
        else:
            print(f"Failed to retrieve the web page. Status code: {response.status_code} for link: {link}")
    except ConnectionError as e:
            print(f"Connection error for link: {link}, skipping...")

    # 随机等待1到4秒
    wait_time = random.uniform(0,1)
    time.sleep(wait_time)

# 处理每个链接文件
for link_file, output_file in zip(link_files, output_files):
    with open(link_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            link = row[0].strip()  # 获取链接，注意去除首尾空白
            process_link(link, output_file)


# 创建一个锁，以防止多个线程同时写入文件
write_lock = threading.Lock()

def process_links(link_file, output_file):
    with open(link_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            link = row[0].strip()  # 获取链接，注意去除首尾空白
            process_link(link, output_file)

def process_a_links():
    link_file = 'a1.csv'
    output_file = 'a_d.csv'
    with write_lock:
        print(f"Processing {link_file} and writing to {output_file}")
    process_links(link_file, output_file)

# 创建两个线程来处理不同的链接文件
a_thread = threading.Thread(target=process_a_links)

# 启动两个线程
a_thread.start()

# 等待两个线程完成
a_thread.join()

    




