import pandas as pd
from crossref.restful import Works


def search_publications(journal_title):
    works = Works()
    query_result = works.query(container_title=journal_title, publisher_name='Wiley-Blackwell')
    return query_result


def process_publications(journal_title):
    publications = search_publications(journal_title)

    # Create empty lists to hold the data
    authors_list = []
    published_dates_list = []
    journal_names_list = []
    affiliations_list = []
    subjects_list = []
    issues_list = []
    volumes_list = []
    published_journal_list = []  # List to hold the specified journal title

    for item in publications:
        # Get the authors
        authors = [f"{author.get('given', '')} {author.get('family', '')}" for author in item.get('author', [])]
        authors_list.append('; '.join(authors))

        # Get the affiliations
        affiliations = [aff.get('name', '') for author in item.get('author', []) for aff in
                        author.get('affiliation', [])]
        affiliations_list.append('; '.join(affiliations))
        # Get the published date
        published_date = '-'.join(str(part) for part in item.get('published-print', {}).get('date-parts', [[]])[0])
        published_dates_list.append(published_date)
        # Get the journal name from the item
        journal_names_list.append(item.get('container-title', [''])[0])

        # Get the subjects
        subjects_list.append('; '.join(item.get('subject', [])))

        # Get the issue and volume
        issues_list.append(item.get('issue', ''))
        volumes_list.append(item.get('volume', ''))

        # Append the specified journal title to the published_journal_list
        published_journal_list.append(journal_title)

    # Create a DataFrame
    data = {
        'Authors': authors_list,
        'Published Date': published_dates_list,
        'Journal Name (from item)': journal_names_list,
        'Published Journal': published_journal_list,  # Include the specified journal title in the data
        'Affiliations': affiliations_list,
        'Subjects': subjects_list,
        'Issue': issues_list,
        'Volume': volumes_list
    }
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv('publications.csv', index=False)


# Define the journal title
journal_title = 'Journal of Industrial Economics'

# Call the function to process the publications and save the data to a CSV file
process_publications(journal_title)