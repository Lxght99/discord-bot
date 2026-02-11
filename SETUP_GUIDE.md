# Setup Guide for Discord Bot

## Introduction
This guide provides detailed instructions for entering code and using the Discord bot. Follow each step carefully to get your bot up and running.

## Prerequisites
- Basic knowledge of programming and Git
- A Discord account
- Node.js installed on your machine (v14 or later)
- A code editor (recommended: Visual Studio Code)

## Step 1: Clone the repository
To get started, you need to clone the repository to your local machine. Open your terminal and run:
```bash
git clone https://github.com/Lxght99/discord-bot.git
cd discord-bot
```

## Step 2: Install dependencies
Once inside the `discord-bot` directory, install all required dependencies by running:
```bash
npm install
```

## Step 3: Create a Discord application
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on the **New Application** button.
3. Name your application and click **Create**.
4. Navigate to the **Bot** tab and click on **Add Bot**.
   - Click **Yes, do it!** to confirm.

## Step 4: Get your bot token
1. In the Bot tab, you will see a section labeled **Token**. Click on **Copy** to save your bot token.
2. **Keep this token private!**

## Step 5: Configure the bot
1. Create a `.env` file in the root directory of your project.
2. Add the following line to your `.env` file:
   ```plaintext
   DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
   ```
   - Replace `YOUR_BOT_TOKEN_HERE` with the token you copied in step 4.

## Step 6: Run the bot
To start the bot, run the following command in your terminal:
```bash
node index.js
```

## Step 7: Invite the bot to your server
1. Go back to the Discord Developer Portal.
2. In the OAuth2 section, under **Scopes**, select **bot**.
3. Under **Bot Permissions**, select the permissions your bot will need.
4. Copy the generated URL and paste it into your browser. Select a server to invite your bot to.

## Step 8: Using the bot
Once the bot is online, you can interact with it in your server. Use commands defined in the bot's code to see its functionalities.

## Troubleshooting
- **Bot not responding?** Ensure it is online in your Discord server.
- **Errors in the terminal?** Check the error messages for clues on what might be wrong.

## Conclusion
You should now have your Discord bot set up and running! Happy coding!