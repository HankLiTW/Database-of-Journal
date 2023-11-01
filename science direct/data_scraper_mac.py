# 更改後
# mac
import cloudscraper
import pandas as pd
import random
import time
from bs4 import BeautifulSoup
import urllib.parse
import json


def data_scraper_redirect(scraper, url):
    response = scraper.get(url)
    random_wait_time = random.uniform(5, 10)
    time.sleep(random_wait_time)
    if response.status_code == 200:
        page_source = response.text
        soup = BeautifulSoup(page_source, 'html.parser')
    else:
        print("fail to open")
        soup = None
    return soup


def data_check(journal_name, redo=False, start=0):
    # store information
    columns = ['Author', 'Affiliation', 'Publication Date', 'Journal Title', 'Title', 'Volume', 'Issue', 'URL']
    result_df = pd.DataFrame(columns=columns)
    # affiliation keywords
    key_words = ["University", "Bank", "Institution", "Sinica", "Department", "Finance", "Economics", "Federal",
                 "College", "Fund","School"]
    # record error
    error_occur = False
    # create scraper
    scraper = cloudscraper.create_scraper()
    if redo == False:
        df = pd.read_csv(f"{journal_name}_api.csv")
    else:
        df = pd.read_csv(f"{journal_name}.csv")
    result_df["URL"] = df["URL"]
    count = start + 1
    total = len(df["URL"])

    for index, row in df.iloc[start:].iterrows():
        url = row["URL"]
        print(url)
        affiliation_list = []
        authors_list = []
        print("open")
        try:
                # sleep not to be detected
                random_wait_object = random.uniform(1, 100)
                if count % 100 == random_wait_object:
                    random_wait_time = random.uniform(60, 80)
                elif count % 500 == 0 and count != 0:
                    random_wait_time = random.uniform(600, 800)
                else:
                    random_wait_time = random.uniform(1,2)
                time.sleep(random_wait_time)
                new_soup = data_scraper_redirect(scraper, url)
                if new_soup:
                    script_tags = new_soup.find_all('script', type='application/json', attrs={"data-iso-key": "_0"})
                    if script_tags:
                        script_tag = script_tags[0]  # Get the first script tag that matches the criteria
                        json_text = script_tag.string or script_tag.text  # Get the text content of the script tag
                        json_data = json.loads(json_text)  # Parse the JSON data
                        # Affiliation
                        authors_content = json_data.get('authors', {}).get('content', [])
                        for author_info in authors_content:
                            for affiliation_info in author_info.get('$$', []):
                                if affiliation_info.get('#name') == 'affiliation':
                                    if affiliation_info:
                                        affiliation_text = affiliation_info.get('$$', [{}])[0].get("_")
                                        if affiliation_text:
                                            contains_key_word = any(key_word in affiliation_text for key_word in key_words)
                                            if contains_key_word:
                                                affiliation_list.append(affiliation_text)
                                            else:
                                                if affiliation_info.get('$$', [{}])[1].get("_"):
                                                    affiliation_text = affiliation_info.get('$$', [{}])[1].get("_")
                                                    affiliation_list.append(affiliation_text)
                        # author name
                        for author_group in json_data['authors'].get('content', []):
                            for author_data in author_group.get('$$', []):
                                if author_data.get('#name') == 'author':
                                    author_info = {}
                                    for field in author_data.get('$$', []):
                                        if field.get('#name') in ['given-name', 'surname']:
                                            field_name = field.get('#name')
                                            field_value = field.get('_')
                                            author_info[field_name] = field_value
                                    authors_list.append(author_info)

                # other information
                volume = new_soup.find('meta', {'name': 'citation_volume'})['content']
                issue = new_soup.find('meta', {'name': 'citation_issue'})['content']
                journal_title = new_soup.find('meta', {'name': 'citation_journal_title'})['content']
                title = new_soup.find('meta', {'name': 'citation_title'})['content']
                publication_date = new_soup.find('meta', {'name': 'citation_publication_date'})['content']
                # integrate
                authors_str = '; '.join(f"{author['given-name']} {author['surname']}" for author in authors_list)
                author_institutions_str = '; '.join(affiliation_list)
                # update df
                result_df.loc[index] = [authors_str, author_institutions_str, publication_date, journal_title, title,
                                        volume, issue, url]
                print(result_df.iloc[index])
                print('success', count, "/", total)
        except Exception as e:
                traceback.print_exc()
                print(f"An error occurred: {e}", count, "/", total)
        finally:
                count += 1
    if error_occur == False:
        result_df['Volume'] = result_df['Volume'].astype(int)
        result_df.sort_values(by='Volume', ascending=False, inplace=True)
        result_df.to_csv(f'{journal_name}.csv', index=False)


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
    journal_list = ["Journal of Financial Economics"]
    for journal in journal_list:
        data_check(journal, redo=False, start=0)
        taiwan_filter(journal)