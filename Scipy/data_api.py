from crossref.restful import Journals
import pandas as pd


def data_api(issn, journal_name):
    authors_list = []
    title_list = []
    affiliations_list = []
    published_dates_list = []
    journal_names_list = []
    subjects_list = []
    volumes_list = []
    issues_list = []
    URL_list = []
    DOI_list = []
    count = 0
    journals = Journals()
    results = journals.works(issn=issn)
    search = results.filter(from_pub_date="2000").select(
        ["container-title", "author", "DOI", "URL", 'subject', 'volume', "title", 'issue', "published-print"])
    total = search.count()
    for item in search:
        authors = [f"{author.get('given', '')} {author.get('family', '')}" for author in item.get('author', [])]
        if len(authors) > 0:
            authors_list.append('; '.join(authors))
            # Get the affiliations
            affiliations = [aff.get('name', '') for author in item.get('author', []) for aff in
                            author.get('affiliation', [])]
            affiliations_list.append('; '.join(affiliations))
            title_list.append(item.get('title', '')[0])
            published_date = '-'.join(str(part) for part in item.get('published-print', {}).get('date-parts', [[]])[0])
            published_dates_list.append(published_date)
            journal_names_list.append(item.get('container-title', [''])[0])
            subjects_list.append('; '.join(item.get('subject', [])))
            volumes_list.append(item.get('volume', ''))
            issues_list.append(item.get('issue', ''))
            URL_list.append(item.get('URL', ''))
            DOI_list.append(item.get('DOI', ''))
            count += 1
            print("load success", count, "/", total)
    data = {
        'Authors': authors_list,
        'Title': title_list,
        'Affiliations': affiliations_list,
        'Published Date': published_dates_list,
        'Journal Name ': journal_names_list,
        'Subjects': subjects_list,
        'Volume': volumes_list,
        'Issue': issues_list,
        'DOI': DOI_list,
        'URL': URL_list

    }
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv(f'{journal_name}_api.csv', index=True)

if __name__ == '__main__':
    data_api(issn='0012-9682', journal_name = 'Econometrica')
    # To use this function, you have to first find ISSN of your intended journal(print is better),
    # and then you have to type the journal's name
