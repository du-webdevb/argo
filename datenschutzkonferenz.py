from bs4 import BeautifulSoup
import pandas as pd
from read_pdf import read_text


def get_data(driver):
    """Args:
        driver : The web driver object that is initialized for scrapping
        
        Returns:
            df: The data frame that contains all scrapped data"""

    try:
        # Open the website
        driver.get("https://www.datenschutzkonferenz-online.de/edsa.html")
        # Get the page source after the search results have loaded
        page_source = driver.page_source
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        # Find all results
        results = soup.find_all("ul", class_="thumbnail_list")
        # Extract links of all available documents
        datenschutzkonferenz_links = []

        for result in results:

            hyperlinks = result.find_all('a')

            for url in hyperlinks:
                datenschutzkonferenz_links.append(
                    ("https://www.datenschutzkonferenz-online.de") + str(url['href'].replace('..', '')))

        table = {'link': [], 'text': []}

        # Extract text from corresponding pdf links
        for pdf_url in datenschutzkonferenz_links:
            text = ''
            text = read_text(pdf_url)
            table['link'].append(pdf_url)
            table['text'].append(text)

        df = pd.DataFrame(table)
        df = df[df['text'] != '']
        df['source_Name'] = "Datenschutzkonferenz"

        return (df)

    except Exception as e:

        return e
