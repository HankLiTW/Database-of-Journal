import traceback
from selenium import webdriver
import pandas as pd
import random
import time
from bs4 import BeautifulSoup
import re


def data_driver(driver, url):
    with open('stealth.min.js', "r") as f:
        js = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })

    driver.get(url)
    # sleep
    random_wait_time = random.uniform(5, 10)
    time.sleep(random_wait_time)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    """
    encoded_url = soup.find('input', {'id': 'redirectURL'})['value']
    redirect_url = urllib.parse.unquote(encoded_url)
    random_wait_time = random.uniform(1,3)
    time.sleep(random_wait_time)
    response = scraper.get(redirect_url)
    new_html = response.text
    new_soup = BeautifulSoup(new_html, 'html.parser')
    """
    return soup


def data_check(journal_name, redo=False, start=0):
    # store information
    columns = ['Author', 'Affiliation', 'Publication Date', 'Journal Title', 'Title', 'Volume', 'URL']
    result_df = pd.DataFrame(columns=columns)
    # record error
    error_occur = False
    if redo == False:
        df = pd.read_csv(f"{journal_name}_api.csv")
        result_df['URL'] = df['URL']
    else:
        df = pd.read_csv(f"{journal_name}.csv")
        result_df = df

    count = start + 1
    total = len(df["URL"])
    for index, row in result_df.iloc[start:].iterrows():
        url = row["URL"]
        print(url)
        affiliation = row["Affiliation"]
        affiliation_list = []
        authors_list = []
        if pd.isna(affiliation):
            print("open")
            try:
                # create scraper
                driver = webdriver.Chrome()
                # sleep not to be detected
                random_wait_object = random.uniform(1, 100)
                if count % 100 == random_wait_object:
                    random_wait_time = random.uniform(60, 80)
                elif count % 500 == 0 and count != 0:
                    random_wait_time = random.uniform(600, 800)
                else:
                    random_wait_time = random.uniform(1, 2)
                time.sleep(random_wait_time)
                soup = data_driver(driver, url)
                if soup:
                    # authors and affiliations
                    authors = soup.find_all(class_='author-name')
                    affiliations = soup.find_all(class_='author-info')
                    if authors:
                        for author in authors:
                            author_name = author.get_text(strip=True)
                            authors_list.append(author_name)
                    if affiliations:
                        for affiliation in affiliations:
                            affiliation_name = affiliation.find('p', string=True).get_text(strip=True)
                            affiliation_list.append(affiliation_name)
                    # other information
                    if soup.find('meta', {'name': 'citation_journal_title'}):
                        journal_title = soup.find('meta', {'name': 'citation_journal_title'})['content']
                    else:
                        journal_title = 0
                    if soup.find('meta', {'name': 'dc.Title'}):
                        title = soup.find('meta', {'name': 'dc.Title'})['content']
                    else:
                        title = 0
                    if soup.find('meta', {'name': 'dc.Date'}):
                        publication_date = soup.find('meta', {'name': 'dc.Date'})['content']
                    else:
                        publication_date = 0
                    if soup.find(class_='article__breadcrumbs separator'):
                        volume_text = soup.find(class_='article__breadcrumbs separator').text
                        volume = re.search(r'Volume (\d+),', volume_text).group(1)
                    else:
                        volume = 0
                    # integrate
                    authors_str = '; '.join(authors_list)
                    author_institutions_str = '; '.join(affiliation_list)
                    # update df
                    result_df.loc[index] = [authors_str, author_institutions_str, publication_date, journal_title,
                                            title, volume, url]
                    print(result_df.iloc[index])
                    if error_occur == False:
                        result_df.to_csv(f'{journal_name}.csv', index=False)
                        print('success, the file has been stored.', count, "/", total)
                    driver.quit()
            except Exception as e:
                traceback.print_exc()
                print(f"An error occurred: {e}", count, "/", total)
            finally:
                count += 1
        else:
            count += 1
            print(f"Skipping {url} as Affiliations is not empty.", count, "/", total)
def taiwan_filter(journal_name):
    taiwan_universities = [
        "National Taiwan University",
        "National Tsing Hua University",
        "National Chiao Tung University",
        "National Cheng Kung University",
        "Taipei Medical University",
        "National Yang Ming University",
        "Chung Yuan Christian University",
        "National Central University",
        "National Sun Yat-sen University",
        "National Taiwan Normal University",
        "National Chung Cheng University",
        "National Taitung University",
        "National Chi Nan University",
        "Tunghai University",
        "National Chengchi University",
        "Soochow University",
        "Chang Gung University",
        "Providence University",
        "Feng Chia University",
        "Tamkang University",
        "I-Shou University",
        "National Taipei University of Technology",
        "Aletheia University",
        "St. John's University",
        "Nanhua University",
        "Chia Nan University of Pharmacy & Science",
        "Tung Fang Design University",
        "Asia University",
        "Ming Chuan University",
        "Kainan University",
        "Chien Hsin University of Science & Technology",
        "Southern Taiwan University of Science & Technology",
        "Takming University of Science & Technology",
        "National Taipei University",
        "Chinese Culture University",
        "National Dong Hwa University",
        "Shih Hsin University",
        "Yuan Ze University",
        "Tzu Chi University",
        "Hsuan Chuang University",
        "Tatung University",
        "National Taiwan Ocean University",
        "National Taipei University of Education",
        "National Ilan University",
        "Chaoyang University of Technology",
        "National Formosa University",
        "Da-Yeh University",
        "Chung Hua University",
        "Far East University",
        "Chung Jen University",
        "Shu-Te University",
        "Shih Chien University",
        "Ta Hwa University",
        "De Lin Institute of Technology",
        "Vanung University",
        "Tungnan University",
        "China Medical University",
        "Fu Jen Catholic University",
        "Chung Yuan Christian University",
        "Chihlee University of Technology",
        "Ming Chuan University",
        "University of Taipei",
        "Kainan University",
        "Tatung University",
        "Chang Gung University",
        "Tzu Chi University",
        "Nanhua University",
        "Tung Fang Design University",
        "Chien Hsin University of Science & Technology",
        "Chaoyang University of Technology",
        "Da-Yeh University",
        "Chung Hua University",
        "Far East University",
        "Chung Jen University",
        "Shu-Te University",
        "Shih Chien University",
        "Ta Hwa University",
        "De Lin Institute of Technology",
        "Vanung University",
        "Tungnan University",
        "China Medical University",
        "Fu Jen Catholic University",
        "Chung Yuan Christian University",
        "Chihlee University of Technology",
        "Ming Chuan University",
        "University of Taipei",
        "Kainan University",
        "Tatung University",
        "Chang Gung University",
        "Tzu Chi University",
        "Nanhua University",
        "Tung Fang Design University",
        "Chien Hsin University of Science & Technology",
        "Academia Sinica",
        "Taiwan"
        'taiwan'
        ".tw"
    ]

    journal = pd.read_csv(f"{journal_name}.csv")
    print("open success")
    # 创建一个条件以判断"Institutions"列是否包含台湾排名前四十大学、"Academia Sinica"和"Jinan University"
    has_taiwan_institutions = journal["Affiliation"].str.contains("|".join(taiwan_universities), case=False, na=False)

    # 筛选包含台湾排名前四十大学、"Academia Sinica"和"Jinan University"的行
    data_taiwan = journal[has_taiwan_institutions]

    # 保存包含台湾排名前四十大学、"Academia Sinica"和"Jinan University"的行为一个新的CSV文件
    file_taiwan = f"{journal_name}_taiwan_scholar.csv"
    data_taiwan.to_csv(file_taiwan, index=False)

    print(f"已提取包含台湾排名前四十大学、Academia Sinica 和 Jinan University 的数据并保存为 {file_taiwan}")


if __name__ == '__main__':
    #範例
    journal_list = ["Journal of Labor Economics"]
    for journal in journal_list:
        data_check(journal, redo=False, start=0)
        taiwan_filter(journal)