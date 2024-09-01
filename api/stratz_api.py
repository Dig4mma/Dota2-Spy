import os
import requests
from dotenv import load_dotenv
import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class StratzAPI:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://api.stratz.com/graphql"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('STRATZ_API_TOKEN')}",
            "Content-Type": "application/json"
        }

    def get_match_data(self, match_id):
        query = f"""
        query Match {{
            match(id: {match_id}) {{
                didRadiantWin
                durationSeconds
                startDateTime
                lobbyType
                rank
                bracket
                players {{
                    playerSlot
                    steamAccountId
                    kills
                    deaths
                    assists
                    steamAccount {{
                        name
                        smurfFlag
                        seasonRank
                    }}
                    hero {{
                        displayName
                    }}
                    networth
                    experiencePerMinute
                    goldPerMinute
                    level
                    heroDamage
                    item0Id
                    item1Id
                    item2Id
                    item3Id
                    item4Id
                    item5Id
                    backpack0Id
                    backpack1Id
                    backpack2Id
                    neutral0Id
                    heroId
                    numLastHits
                    numDenies
                }}
            }}
        }}
        """

        logger.debug(f"Sending request to {self.base_url} for match ID {match_id}")

        response = requests.post(self.base_url, json={'query': query}, headers=self.headers)

        if response.status_code == 200:
            logger.debug(f"Query successful: {response.status_code}")
            return response.json()
        else:
            logger.error(f"Query failed with status code {response.status_code}: {response.text}")
            raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    # Example usage
    api = StratzAPI()
    try:
        match_data = api.get_match_data(7897159898)
        print(match_data)
    except Exception as e:
        logger.error(f"Failed to fetch match data: {str(e)}")