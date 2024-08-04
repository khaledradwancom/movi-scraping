import requests
from bs4 import BeautifulSoup as bs
import re
import string

# Define the root URL
root = 'https://subslikescript.com'

# Loop through each letter from A to Z
for letter in string.ascii_uppercase:
    url = f'{root}/movies_letter-{letter}'
    response = requests.get(url)
    content = response.text
    soup = bs(content, 'lxml')

    # Find pagination and last page number
    pagination = soup.find('ul', class_='pagination')
    if pagination:
        pages = pagination.find_all('li', class_='page-item')
        if pages:
            last_page = pages[-2].get_text()
        else:
            last_page = '1'
    else:
        last_page = '1'

    # Loop through each page
    for page in range(1, int(last_page) + 1):
        page_url = f'{url}?page={page}'
        response = requests.get(page_url)
        content = response.text
        soup = bs(content, 'lxml')

        box = soup.find('article', class_='main-article')
        if box:
            links = [a['href'] for a in box.find_all('a', href=True)]
            print(f'Total links found on page {page} for letter {letter}: {len(links)}')

            # Loop through each link
            for link in links:
                script_url = f'{root}{link}'
                response = requests.get(script_url)
                content = response.text
                soup = bs(content, 'lxml')

                box = soup.find('article', class_='main-article')

                if box:
                    title = box.find('h1').get_text() if box.find('h1') else 'Untitled'  # Get the title of the script
                    script_element = box.find('div', class_='full-script')

                    if script_element:
                        script = script_element.get_text(strip=True, separator='\n')  # Get the script text

                        # Clean the title to make it a valid filename
                        valid_title = re.sub(r'[\\/*?:"<>|]', "", title)

                        # Write the script to a text file
                        try:
                            with open(f'{valid_title}.txt', 'w', encoding='utf-8') as file:
                                file.write(script)
                            print(f'Script saved successfully as {valid_title}.txt')
                        except Exception as e:
                            print(f'Error saving script: {e}')
                    else:
                        print('Script element not found')
                else:
                    print('Main article not found')
        else:
            print(f'No main article found on page {page} for letter {letter}')
