import random
import time
from bs4 import BeautifulSoup
import requests
import csv
import os
from concurrent.futures import ThreadPoolExecutor

# Set the user agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Define a function to extract and save links with random delays
def extract_and_save_links_with_delay(input_csv_filename, output_csv_filename):
    with open(input_csv_filename, mode="r") as input_file, open(output_csv_filename, mode="w", newline='') as output_file:
        csv_reader = csv.reader(input_file)
        next(csv_reader)  # Skip the header row

        writer = csv.writer(output_file)
        writer.writerow(["Article Link"])  # Write the header row

        for row in csv_reader:
            article_link = row[0]
            response = requests.get(article_link, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract article links

                article_links = soup.select('a.article-content-title')

                for link in article_links:
                    article_url = "https://www.sciencedirect.com" + link["href"]
                    writer.writerow([article_url])

                print(f"Successfully extracted links and wrote to {output_csv_filename}")

                # Add a random delay between requests (e.g., 2 to 5 seconds)
                delay_seconds = random.uniform(2, 5)
                time.sleep(delay_seconds)
            else:
                print(f"Failed to retrieve web content: {article_link}")

# Modify the process_csv_files function to include delays
def process_csv_files_with_delay():
    input_files = ["a.csv", "b.csv", "c.csv"]
    
    with ThreadPoolExecutor(max_workers=len(input_files)) as executor:
        for input_file in input_files:
            # Construct the output file name, for example, converting "a.csv" to "a_output.csv"
            output_file = f"{os.path.splitext(input_file)[0]}_output.csv"
            executor.submit(extract_and_save_links_with_delay, input_file, output_file)
            
            # Add a random delay between starting threads (e.g., 2 to 5 seconds)
            delay_seconds = random.uniform(2, 5)
            time.sleep(delay_seconds)

# Usage example
process_csv_files_with_delay()








