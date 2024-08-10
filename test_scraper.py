from scrapers.dotabuff_scraper import DotabuffScraper

def test_recent_matches(player_id):
    scraper = DotabuffScraper(player_id)
    try:
        matches = scraper.get_data('recent_matches')
        if matches:
            print(f"Recent matches for account {player_id}:")
            for match in matches:
                print(f"Hero: {match['hero']}")
                print(f"Result: {match['result']}")
                print(f"Type: {match['type']}")
                print(f"Duration: {match['duration']}")
                print(f"KDA: {match['kda']}")
                print(f"Lobby Bracket: {match['lobby_bracket']}")
                print("-" * 20)
        else:
            print(f"No matches found for account {player_id}.")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_overview(player_id):
    scraper = DotabuffScraper(player_id)
    try:
        overview = scraper.get_data('overview')
        if overview:
            print(f"Overview for account {player_id}:")
            print(f"Name: {overview.get('name')}")
            print(f"Rank: {overview.get('rank')}")
        else:
            print(f"No overview data found for account {player_id}.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    player_id = input("Enter a player ID to test: ")
    print("\nTesting Recent Matches...")
    test_recent_matches(player_id)
    print("\nTesting Overview...")
    test_overview(player_id)