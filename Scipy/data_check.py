# formal
import cloudscraper
import pandas as pd
import random
import time
from bs4 import BeautifulSoup


def data_check(journal_name, redo=False, start=0):
    # create cloudscraper
    scraper = cloudscraper.create_scraper()
    if redo == False:
        df = pd.read_csv(f"{journal_name}_api.csv", index_col=0)
    else:
        df = pd.read_csv(f"{journal_name}.csv", index_col=0)
    count = start+1
    total = len(df["URL"])

    for index, row in df.iloc[start:].iterrows():
        url = row["URL"]
        print(url)
        affiliation = row["Affiliations"]

        # check affiliation
        if pd.isna(affiliation) or df.iloc[index]["Title"] == df.iloc[index - 1]["Title"]:
            print("open")
            try:
                # to URL
                response = scraper.get(url)
                random_wait_object = random.uniform(1, 100)
                if count % 100 == random_wait_object:
                    random_wait_time = random.uniform(60, 80)
                elif count % 400 == 0:
                    random_wait_time = random.uniform(600, 1000)
                else:
                    random_wait_time = random.uniform(5, 12)
                time.sleep(random_wait_time)
                if response.status_code == 403:
                    print(403, "error occur", index, url)
                    df.to_csv(f'{journal_name}.csv', index=True)
                    time.sleep(1000)
                    #keep doing
                    data_check(journal_name, redo=True, start=index)
                if response.status_code == 200:
                    print("open success")
                    # get html
                    page_source = response.text

                    # parse html by beatifulsoup
                    soup = BeautifulSoup(page_source, 'html.parser')

                    # get author
                    authors = [meta['content'] for meta in soup.find_all('meta', {'name': 'citation_author'})]

                    # get citation_author_institution
                    author_institutions = [meta['content'] for meta in soup.find_all('meta', {'name': 'moreInfoLink'})]

                    # get citation_publication_date
                    publication_date = soup.find('meta', {'name': 'citation_publication_date'})['content'] if soup.find(
                        'meta', {'name': 'citation_publication_date'}) else None

                    # get citation_title
                    title = soup.find('meta', {'name': 'citation_title'})['content'] if soup.find('meta', {
                        'name': 'citation_title'}) else None
                    authors_str = '; '.join(authors)
                    author_institutions_str = '; '.join(author_institutions)
                    # update df
                    df.at[index, 'Authors'] = authors_str
                    df.at[index, 'Affiliations'] = author_institutions_str
                    df.at[index, 'Published Date'] = publication_date
                    df.at[index, 'Title'] = title
                    print(df.iloc[index])
                    print('success', count, "/", total)
                else:
                    print(f"Failed to retrieve: {response.status_code}", count, "/", total)
            except Exception as e:
                print(f"An error occurred: {e}", count, "/", total)
            finally:
                count += 1
        else:
            count += 1
            print(f"Skipping {url} as Affiliations is not empty.", count, "/", total)

    # save CSV
    df.to_csv(f'{journal_name}.csv', index=True)

if __name__ == "__main__":
    data_check('Econometrica', redo=False, start=0)
    #journal name, redo = true means you have run this function previously, and you want to keep collecting data
    # start means where the collection begin, for example, if start = 0, this function will start collect data from index = 0
