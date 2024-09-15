from datetime import datetime
from requests import get
from bs4 import BeautifulSoup
from pathlib import Path
from json import dump

IVOIREBUSINESS_URL = 'https://www.ivoirebusiness.net/'
timestamp = f'{datetime.now().strftime("%d-%m-%Y")}_{datetime.now().strftime("%X").replace(":", "")}'
DIR = Path().cwd() / 'actu'
DIR.mkdir(exist_ok=True, parents=True)


def get_ivoirebusiness():
    
    # Getting website
    g = get(IVOIREBUSINESS_URL)
    print(f'Ivoirebusiness - Status_code : {g.status_code}')
    soup = BeautifulSoup(g.content, 'html.parser')
    
    # Sorting
    soup.find(id='block-views-recent-videos-block').decompose()
    soup.find(id='block-views-titrologie-block').decompose()
    soup.find('img').decompose()

    # Getting news
    h2 = soup.find(class_='region region-content').find_all('h2')
    
    news = {}
    article_number = 0
    for title in h2:
        title_link = title.find('a')['href'].removeprefix('/')
        actu_soup = BeautifulSoup(get(f'{IVOIREBUSINESS_URL}{title_link}').content, 'html.parser')

        # Sorting
        actu_soup.find(id='sidebar-first').decompose()
        actu_soup.find(class_='span4').decompose()
        actu_soup.find(id='block-block-25').decompose()

        publication_date = actu_soup.find(class_='submitted')
        publication_list = actu_soup.find_all(class_='field-item even')
        i = 0
        '''
        @todo : Play with CSS to win the War
        '''
        for topic in publication_list:
            if len(topic.text) < (len(title) + 120) or 'pat' in topic.text[:3].lower() or 'par' in topic.text[:3].lower():
                i += 1
            else:
                break

        article_data = {
            'title': title.text.strip(),
            'url': f'{IVOIREBUSINESS_URL}{title_link}',
            'prev': actu_soup.find('img')['src'],
            'topic': publication_list[i].text.strip(),
            'date': publication_date.text.strip().removesuffix('.')
        }
        news[article_number] = article_data
        article_number += 1

        # print('\n', prev, '\n', f'*****\n{article_data["title"]} : {ivoirebusiness_url}{np}\n Topic : \n[\n{article_data["topic"]}\n]\n\n')
        print(f'Getting : {article_data["title"]}')
    
    filepath = DIR / f'actu_{timestamp}.json'
    print(f'Saved in : {filepath}')
    with open(filepath, 'w+', encoding='utf-8') as f:
        dump(news, f, ensure_ascii=False, indent=4)

    return filepath
