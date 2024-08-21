# Dota2 Spy

## Description
Dota2 Spy is a feature-rich Discord bot designed to provide real-time information and detailed statistics for Dota 2 players. The bot fetches data from reliable sources and presents it in a user-friendly manner, enhancing your Dota 2 experience directly within Discord.

## Features
- **Player Profiles & Match History**: Retrieve comprehensive player profiles and detailed match histories, including recent matches, win rates, and KDA statistics.
- **Hero Statistics**: Access in-depth statistics for all Dota 2 heroes, including win rates, popular builds, and role-based performance.
- **Real-Time Game Updates**: Get live updates on ongoing games, player performance, and match outcomes.
- **Interactive UI**: Utilize buttons, select menus, and modals for an interactive and seamless user experience.
- **Multi-Server Support**: Easily integrate and use the bot across multiple Discord servers.
- **Error Handling**: Robust error handling ensures that users receive informative messages when something goes wrong.

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
3. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Create a new Discord bot**: 
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications), create a new application, and add a bot to it.
   - Obtain the bot token from the "Bot" section of your application.

2. **Set up your environment variables**:
   - Create a `.env` file in the root directory of the project and add your bot token:
     ```
     TOKEN=YOUR_DISCORD_BOT_TOKEN
     ```

3. **Run the bot**:
   ```bash
   python bot.py
   ```

4. **Invite the bot to your server**:
   - Go to the OAuth2 section of the Developer Portal, select "bot" under "scopes", and choose the required permissions.
   - Copy the generated URL and use it to invite the bot to your server.

## Commands and Interactions
- **/dota**: Opens the main view for Dota 2 analysis, including options to search for player profiles or specific matches.

## Contributing
Contributions are highly encouraged! If you have any ideas, bug reports, or improvements, please open an issue or submit a pull request.

### Steps to Contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes, ensuring to follow the existing code style.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request and describe your changes in detail.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

