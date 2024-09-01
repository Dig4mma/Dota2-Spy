# Dota2 Spy

## Description
Dota2 Spy is a powerful Discord bot designed to provide real-time information and statistics for Dota 2 players. It fetches data from the official Dota 2 API and Stratz API and presents it in a user-friendly manner, enhancing your Dota 2 experience.

## Installation

### Prerequisites
- Python 3.8 or higher
- Discord account and server where you have permission to add bots

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/dota2-spy.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd dota2-spy
   ```
3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Create a new Discord bot** and obtain the bot token from the [Discord Developer Portal](https://discord.com/developers/applications).
2. **Add your bot token and Stratz API key to a `.env` file**:
   ```
   TOKEN=YOUR_DISCORD_BOT_TOKEN
   STRATZ_API_KEY=YOUR_STRATZ_API_BEARER_TOKEN
   ```
3. **Run the bot**:
   ```bash
   python bot.py
   ```

## Features
- **Fetch Player Profiles and Match History**: Retrieve comprehensive player profiles and detailed match histories using the Dotabuff scraper.
- **Fetch Match Data from Stratz API**: Use the Stratz API to retrieve detailed match data including player statistics, hero performance, and match outcomes.
- **Real-Time Game Updates**: Get live updates on ongoing games and player performance.
- **Hero Statistics and Win Rates**: Access in-depth statistics for all Dota 2 heroes, including win rates and popular builds.
- **Multi-Server Support**: Easily integrate and use the bot across multiple Discord servers.

## Contributing
Contributions are welcome! If you have any ideas or improvements, feel free to open an issue or submit a pull request.

### Steps to Contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

