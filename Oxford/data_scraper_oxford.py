#Oxford
import traceback
import cloudscraper
import pandas as pd
import random
import time
from bs4 import BeautifulSoup
import json


def data_scraper_redirect(scraper, url):
    response = scraper.get(url)
    random_wait_time = random.uniform(8, 13)
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
    columns = ['Author', 'Affiliation', 'Publication Date', 'Journal Title', 'Title', 'Volume', 'URL']
    result_df = pd.DataFrame(columns=columns)
    # record error
    error_occur = False
    # create scraper
    scraper = cloudscraper.create_scraper()
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
        print("open")
        publication_date, journal_title, title = 0,0,0
        if pd.isna(affiliation):
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
                    soup = data_scraper_redirect(scraper, url)
                    if soup:
                        script_tags = soup.find_all('script')
                        for script_tag in script_tags:
                            if script_tag.string:
                                try:
                                    json_data = json.loads(script_tag.string)  # Parse the JSON data
                                    if 'author' in json_data:
                                        authors_info = json_data['author']
                                        if authors_info:
                                            for author in authors_info:
                                                authors_list.append(author['name'])
                                            # affiliation
                                            for affiliation in authors_info:
                                                affiliation_list.append(affiliation['affiliation'])
                                        # title
                                        title = json_data['name']
                                        # date
                                        publication_date = json_data['datePublished']
                                        # publication_title
                                        journal_title = json_data['isPartOf']['isPartOf']['name']
                                except:
                                    continue

                        # Parse the JSON data
                       # json_text = script_tag.string or script_tag.text  # Get the text content of the script tag
                        #authors
                        #volumn
                        volume_tag = soup.find('meta', attrs={'name': 'citation_volume'})
                        volume = volume_tag['content']
                        #integrate
                        authors_str = '; '.join(authors_list)
                        author_institutions_str = '; '.join(affiliation_list)
                        # update df
                        result_df.loc[index] = [authors_str, author_institutions_str, publication_date, journal_title, title, volume, url]
                        print(result_df.iloc[index])
                        if error_occur == False:
                            result_df.to_csv(f'{journal_name}.csv', index=False)
                            print('success, the file has been stored.', count, "/", total)
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
    journal_list = ["The Quarterly Journal of Economics","The Review of Financial Studies"]
    for journal in journal_list:
        data_check(journal, redo=False, start=0)
        taiwan_filter(journal)