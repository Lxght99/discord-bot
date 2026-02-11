# Discord Moderation Bot

A powerful Discord moderation bot built with discord.py that helps keep your server clean and organized.

## Features

### User Moderation
- **Warn** - Issue warnings to users with reasons
- **Mute** - Temporarily or permanently mute users
- **Unmute** - Remove mutes from users
- **Kick** - Remove users from the server
- **Ban** - Permanently ban users from the server

### Message Moderation
- **Word Filter** - Automatically delete messages containing filtered words
- **Spam Detection** - Automatically mute users who spam messages
- **Filter Management** - Add, remove, and view filtered words

### Database Support
- SQLite database for persistent storage of:
  - User warnings
  - Mute records
  - Ban records
  - Filtered words

## Installation

### Prerequisites
- Python 3.8+
- Discord Bot Token

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Lxght99/discord-bot.git
   cd discord-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   DATABASE_PATH=moderation.db
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

## Commands

### User Moderation Commands

#### /warn
Warn a user for rule violations
```
/warn user:<user> reason:<reason>
```
**Permissions Required:** Moderate Members

#### /warnings
Check all warnings for a user
```
/warnings user:<user>
```

#### /mute
Mute a user for a specified duration
```
/mute user:<user> duration:<minutes> reason:<reason>
```
- Duration: 0 for indefinite mute
- Permissions Required: Moderate Members

#### /unmute
Remove a mute from a user
```
/unmute user:<user>
```
**Permissions Required:** Moderate Members

#### /kick
Kick a user from the server
```
/kick user:<user> reason:<reason>
```
**Permissions Required:** Kick Members

#### /ban
Ban a user from the server
```
/ban user:<user> reason:<reason>
```
**Permissions Required:** Ban Members

### Message Moderation Commands

#### /filter_add
Add a word to the filter list
```
/filter_add word:<word>
```
**Permissions Required:** Manage Messages

#### /filter_remove
Remove a word from the filter list
```
/filter_remove word:<word>
```
**Permissions Required:** Manage Messages

#### /filters
View all filtered words in the server
```
/filters
```

## Database Schema

### warnings table
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER)
- guild_id (INTEGER)
- moderator_id (INTEGER)
- reason (TEXT)
- timestamp (DATETIME)

### mutes table
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER)
- guild_id (INTEGER)
- moderator_id (INTEGER)
- reason (TEXT)
- mute_time (DATETIME)
- is_active (BOOLEAN)
- timestamp (DATETIME)

### bans table
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER)
- guild_id (INTEGER)
- moderator_id (INTEGER)
- reason (TEXT)
- timestamp (DATETIME)

### message_filters table
- id (INTEGER PRIMARY KEY)
- guild_id (INTEGER)
- word (TEXT UNIQUE)
- action (TEXT)
- timestamp (DATETIME)

## Project Structure

```
discord-bot/
├── main.py              # Bot entry point
├── database.py          # Database operations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore file
├── README.md           # This file
└── cogs/
    ├── moderation.py          # User moderation commands
    └── message_moderation.py  # Message moderation commands
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License.

## Support

For support, please create an issue in the repository.