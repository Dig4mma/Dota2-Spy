import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
from datetime import datetime

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
        match_elements = soup.select('section article table tbody tr')  # Select all matches

        for match in match_elements:
            match_data = {}
            hero_element = match.select_one('td.cell-large a')
            result_element = match.select_one('td:nth-child(4) a')
            type_element = match.select_one('td:nth-child(5)')
            duration_element = match.select_one('td:nth-child(6)')
            kda_element = match.select_one('td:nth-child(7)')
            lobby_bracket_element = match.select_one('td:nth-child(2) div')
            date_element = match.select_one('td:nth-child(4) time')
            role_element = match.select_one('td:nth-child(3).cell-centered.r-none-mobile')

            if hero_element:
                match_data['hero'] = hero_element.text.strip()
                href = hero_element.get('href', '')
                if href:
                    match_data['match_id'] = href.split('/')[-1]  # Extract the match ID from the href
            else:
                match_data['hero'] = 'Unknown'
                match_data['match_id'] = 'Unknown'

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

            if date_element:
                timestamp = date_element['datetime']
                match_data['date'] = self.calculate_time_difference(timestamp)
            else:
                match_data['date'] = 'Unknown'

            if role_element:
                role = self.parse_role(role_element)
                match_data['role'] = role
            else:
                match_data['role'] = 'Unknown'

            matches.append(match_data)

        return matches

    def calculate_time_difference(self, timestamp):
        match_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        now = datetime.now(match_time.tzinfo)
        diff = now - match_time

        if diff.days >= 365:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
        elif diff.days >= 30:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        elif diff.days >= 7:
            weeks = diff.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif diff.days >= 1:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"

    def parse_role(self, role_element):
        icons = role_element.find_all('i')
        roles = [icon.get('title', '') for icon in icons if 'title' in icon.attrs]

        if 'Core Role' in roles:
            if 'Safe Lane' in roles:
                return 'Safe Lane'
            elif 'Off Lane' in roles:
                return 'Off Lane'
            elif 'Mid Lane' in roles:
                return 'Mid Lane'
        elif 'Support Role' in roles:
            if 'Safe Lane' in roles:
                return 'Hard Support'
            elif 'Off Lane' in roles:
                return 'Support'

        return 'Unknown'

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
        
        # Extract profile image URL
        profile_image_element = soup.select_one('img.image-player.image-bigavatar')
        if profile_image_element and 'src' in profile_image_element.attrs:
            overview_data['profile_image'] = profile_image_element['src']
        else:
            overview_data['profile_image'] = 'Unknown'
        
        # Extract rank image URL
        rank_image_element = soup.select_one('img.rank-tier-base')
        if rank_image_element and 'src' in rank_image_element.attrs:
            overview_data['rank_image'] = rank_image_element['src']
        else:
            overview_data['rank_image'] = 'Unknown'
        
        return overview_data