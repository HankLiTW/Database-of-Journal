import random
import time
from bs4 import BeautifulSoup
from selenium import webdriver
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
def data_driver(driver, url):
    with open('stealth.min.js', "r") as f:
        js = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })

    driver.get(url)
    #sleep
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
def extract_and_save_links_with_delay(input_csv_filename, output_csv_filename,start_index=0):
    with open(input_csv_filename, mode="r") as input_file, open(output_csv_filename, mode="w", newline='') as output_file:
        print('open successfully', input_file, output_file)
        csv_reader = csv.reader(input_file)
        next(csv_reader)  # Skip the header row

        writer = csv.writer(output_file)
        writer.writerow(["URL"])  # Write the header row

        current_index = 0
        for row in csv_reader:
            if current_index >= start_index:
                driver = webdriver.Chrome()
                article_link = row[0]
                headers = {'User-Agent': random.choice(user_agents)}  # Choose a random user agent
                #if response.status_code == 200:
                print(f"Successfully retrieved web content: {article_link}")
                soup = data_driver(driver, article_link)
                # Extract article links
                article_links = soup.find_all('h4', {'class': 'issue-item__title'})
                print(article_links)
                if article_links:
                    for article_tag in article_links:
                        link_tage = article_tag.find('a')
                        if link_tage:
                            href = link_tage['href']
                            article_url = "https://www.journals.uchicago.edu" + href
                            print(article_url)
                            writer.writerow([article_url])
                            output_file.flush()
                            print("successfully write url to file")# 将链接写入输出文件
                            print(f"Successfully extracted links and wrote to {output_csv_filename}")



                    # Add a random delay between requests (e.g., 2 to 5 seconds)
                delay_seconds = random.uniform(5,10)
                time.sleep(delay_seconds)
                driver.close()
            else:
                print(f"Failed to retrieve web content: {article_link}")
        current_index += 1





if __name__ == "__main__":

    journal_list = ["Journal of Labor Economics","Journal of Political Economy","The Journal of Law and Economics"]
    #with ThreadPoolExecutor(max_workers=len(journal_list)) as executor:
    for input_file in journal_list:
            # Set the output file name to "Journal of Development Economics.csv" for all input files
            input_file_url = f"{input_file}_url.csv"
            output_file = f"{input_file}_api.csv"
            #executor.submit(extract_and_save_links_with_delay, input_file_url, output_file,start_index=36)
            extract_and_save_links_with_delay(input_file_url, output_file, start_index=0)















