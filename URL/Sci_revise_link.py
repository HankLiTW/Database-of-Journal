# Read the CSV file into a DataFrame
import pandas as pd

# Function to correct the URL format
def correct_url(url,journal_name):
    parts = url.split("/")
    print(parts)
    if 'vol' not in parts:
        index = parts.index(journal_name) + 1
        parts.insert(index, 'vol')
    return "/".join(parts)

journal_list = ["Journal of Economic Theory","Journal of Financial Economics",'Journal of International Economics','Journal of Monetary Economics','Journal of Urban Economics','Review of Economic Dynamics']
for journal_name in journal_list:
    df = pd.read_csv(f'{journal_name}_url.csv')
    # Apply the function to correct URLs
    df.rename(columns={'Links': 'URL'}, inplace=True)
    journal_name_formatted = journal_name.replace(" ", "-").lower()
    df['URL'] = df['URL'].apply(lambda url: correct_url(url, journal_name_formatted))
    # Drop duplicates
    df = df.drop_duplicates(subset=['URL'])

    # Write the corrected DataFrame to a new CSV file
    df.to_csv(f'{journal_name}_url.csv', index=False)