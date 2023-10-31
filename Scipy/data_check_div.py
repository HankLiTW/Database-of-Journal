# formal
import cloudscraper
import pandas as pd
import random
import time
from bs4 import BeautifulSoup


def data_check_by_div(journal_name, redo=False, start=0):
    keywords = ['university', 'institution', 'academia sinica', 'school']
    error_occur = False
    # create cloudscraper
    scraper = cloudscraper.create_scraper()
    if redo == False:
        df = pd.read_csv(f"{journal_name}_api.csv", index_col=0)
    else:
        df = pd.read_csv(f"{journal_name}.csv", index_col=0)
    count = start + 1
    total = len(df["DOI"]) + 1

    for index, row in df.iloc[start:].iterrows():
        url = "https://onlinelibrary.wiley.com/doi/abs/" + row["DOI"]
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
                    data_check_by_div(journal_name, redo=True, start=index)
                    error_occur = True
                    break
                if response.status_code == 200:
                    print("open success")
                    # get html
                    page_source = response.text

                    # parse html
                    soup = BeautifulSoup(page_source, 'html.parser')
                    # get author
                    desktop_authors_div = soup.find('div', class_='loa-wrapper loa-authors hidden-xs desktop-authors')
                    if desktop_authors_div:
                        # find all author_div
                        author_info_divs = desktop_authors_div.find_all('div',
                                                                        class_='author-info accordion-tabbed__content')

                        # empty list to store affiliation information
                        author_institutions = []

                        # go through author-info div
                        for div in author_info_divs:
                            if any(keyword.lower() in div.text.lower() for keyword in keywords):
                                # if containing keywords, save affiliation
                                author_institutions.append(div.text)

                    else:
                        print(f"No desktop_authors_div found for URL: {url}")
                        author_institutions = []

                    # get author
                    # authors = [meta['content'] for meta in soup.find_all('meta', {'name': 'citation_author'})]

                    # get citation_author_institution
                    # author_institutions = [meta['content'] for meta in soup.find_all('meta', {'name': 'moreInfoLink'})]

                    # get  citation_publication_date
                    publication_date = soup.find('meta', {'name': 'citation_publication_date'})['content'] if soup.find(
                        'meta', {'name': 'citation_publication_date'}) else None

                    # get citation_title
                    title = soup.find('meta', {'name': 'citation_title'})['content'] if soup.find('meta', {
                        'name': 'citation_title'}) else None
                    # authors_str = '; '.join(authors)
                    author_institutions_str = '; '.join(author_institutions)
                    # update df
                    # df.at[index, 'Authors'] = authors_str
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
    if error_occur == False:
        df.to_csv(f'{journal_name}.csv', index=True)

if __name__ == '__main__':
    data_check_by_div("Journal of Finance",redo=False,start=0)
    # same as data_check function, but find data from div( if the website structure is complicated)