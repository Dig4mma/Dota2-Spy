import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper

class DotabuffScraper(BaseScraper):
    BASE_URL = 'https://www.dotabuff.com/players/'

    def __init__(self, player_id):
        self.player_id = player_id

    def get_data(self, data_type):
        url = self.BASE_URL + str(self.player_id)
        if data_type == 'recent_matches':
            url += "/matches"
        elif data_type == 'overview':
            url += "/"
        else:
            raise ValueError(f"Unknown data type: {data_type}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return self.parse_data(response.text, data_type)
        else:
            raise Exception(f"Failed to retrieve data: {response.status_code} for URL {url}")

    def parse_data(self, html_content, data_type):
        soup = BeautifulSoup(html_content, 'html.parser')
        if data_type == 'recent_matches':
            return self.parse_recent_matches(soup)
        elif data_type == 'overview':
            return self.parse_overview(soup)
        else:
            raise ValueError(f"Unknown data type: {data_type}")

    def parse_recent_matches(self, soup):
        matches = []
        match_elements = soup.select('section article table tbody tr')[:10]  # Select only the first 10 matches

        for match in match_elements:
            match_data = {}
            hero_element = match.select_one('td.cell-large a')
            result_element = match.select_one('td:nth-child(4) a')
            type_element = match.select_one('td:nth-child(5)')
            duration_element = match.select_one('td:nth-child(6)')
            kda_element = match.select_one('td:nth-child(7)')
            lobby_bracket_element = match.select_one('td:nth-child(2) div')

            if hero_element:
                match_data['hero'] = hero_element.text.strip()
            else:
                match_data['hero'] = 'Unknown'

            if result_element:
                match_data['result'] = result_element.text.replace(' Match', '').strip()
            else:
                match_data['result'] = 'Unknown'

            if type_element:
                match_data['type'] = type_element.contents[0].strip() if type_element.contents else 'Unknown'
            else:
                match_data['type'] = 'Unknown'

            if duration_element:
                match_data['duration'] = duration_element.text.strip()
            else:
                match_data['duration'] = 'Unknown'

            if kda_element:
                match_data['kda'] = kda_element.text.strip()
            else:
                match_data['kda'] = 'Unknown'

            if lobby_bracket_element:
                match_data['lobby_bracket'] = lobby_bracket_element.text.strip()
            else:
                match_data['lobby_bracket'] = 'Unknown'

            matches.append(match_data)

        return matches

    def parse_overview(self, soup):
        overview_data = {}
        
        # Extract player name
        name_element = soup.select_one('h1')
        if name_element:
            name = name_element.text.strip()
            if name.endswith("Overview"):
                name = name[: -len("Overview")].strip()
            overview_data['name'] = name
        else:
            overview_data['name'] = 'Unknown'
        
        # Extract player rank
        rank_element = soup.select_one('.rank-tier-wrapper')
        if rank_element and 'title' in rank_element.attrs:
            rank = rank_element['title'].replace('Rank: ', '').strip()
            overview_data['rank'] = rank
        else:
            overview_data['rank'] = 'Unknown'
        
        return overview_data