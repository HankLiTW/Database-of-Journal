import random
import time
from bs4 import BeautifulSoup
import cloudscraper
import csv
#from concurrent.futures import ThreadPoolExecutor

# Define a list of user agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Firefox/100.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1000.100 Safari/537.36'
]
# Define a function to extract and save links with random delays
def extract_and_save_links_with_delay(input_csv_filename, output_csv_filename,start_index=0):
    with open(input_csv_filename, mode="r") as input_file, open(output_csv_filename, mode="a", newline='') as output_file:
        print('open successfully', input_file, output_file)
        scraper = cloudscraper.create_scraper()
        csv_reader = csv.reader(input_file)

        writer = csv.writer(output_file)
        if start_index ==0:
            writer.writerow(["URL"])  # Write the header row

        current_index = 0
        for row in csv_reader:
            if current_index >= start_index:
                article_link = row[0]
                headers = {'User-Agent': random.choice(user_agents)}  # Choose a random user agent
                response = scraper.get(article_link,headers=headers)
                if response.status_code == 200:
                    print(f"Successfully retrieved web content: {article_link}")
                    soup = BeautifulSoup(response.text, 'html.parser')
                    print(soup)
                    # Extract article links
                    if soup.find('h4', string='ARTICLES'):
                        h4_tag = soup.find('h4', string='ARTICLES')
                    elif soup.find('h4', string='Articles'):
                        h4_tag = soup.find('h4', string='Articles')
                    else:
                        h4_tag = soup.find('h4', string='Research Article')

                    # If the h4 tag is found, locate the parent div of h4
                    if h4_tag:
                        parent_div = h4_tag.find_parent('div')

                        # Locate the h3 tags within the parent div
                        h3_tags = parent_div.find_all('h3')

                        # Iterate through the h3 tags and extract href attribute from a tags
                        for h3_tag in h3_tags:
                            a_tag = h3_tag.find('a', {'class': 'part-link'})
                            if a_tag:
                                href = a_tag['href']
                                if 'cover-and-front-matter' not in href and 'cover-and-back-matter' not in href:
                                    article_url = "https://www.cambridge.org" + href
                                    print(article_url)
                                    writer.writerow([article_url])
                                    output_file.flush()
                                    print("successfully write url to file")# 将链接写入输出文件
                                    print(f"Successfully extracted links and wrote to {output_csv_filename}")

                    else:
                        print('h4 tag with text "Articles" not found')

                    # Add a random delay between requests (e.g., 2 to 5 seconds)
                    delay_seconds = random.uniform(5,10)
                    time.sleep(delay_seconds)
                else:
                    print(f"Failed to retrieve web content: {article_link}")
            current_index += 1



def data_scraper_redirect(scraper, url):
    response = scraper.get(url)
    if response.status_code == 200:
        page_source = response.text
        soup = BeautifulSoup(page_source, 'html.parser')
    else:
        print("fail to open")
        soup = None
    return soup
def find_soup():
    scraper = cloudscraper.create_scraper()
    url = 'https://www.cambridge.org/core/journals/journal-of-economic-history/issue/11D3795BCF82D40EA83C5F96ABA9CEFF'
    soup = data_scraper_redirect(scraper, url)

    return(soup)


if __name__ == "__main__":
    journal_list = ["The Journal of Economic History"]
    #with ThreadPoolExecutor(max_workers=len(journal_list)) as executor:
    for input_file in journal_list:
            # Set the output file name to "Journal of Development Economics.csv" for all input files
            input_file_url = f"{input_file}_all_issues.csv"
            output_file = f"{input_file}_api.csv"
            #executor.submit(extract_and_save_links_with_delay, input_file_url, output_file,start_index=36)
            extract_and_save_links_with_delay(input_file_url, output_file, start_index=0)














