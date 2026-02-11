import discord
from discord.ext import commands
from discord import app_commands
import database
import re

class MessageModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_cache = {{}}  # {{user_id: [timestamps]}}
        self.spam_threshold = 5  # 5 messages
        self.spam_timeframe = 5  # within 5 seconds

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Monitor messages for spam and filtered words."""
        if message.author.bot:
            return

        guild_id = message.guild.id if message.guild else None
        if not guild_id:
            return

        # Check for filtered words
        await self.check_filtered_words(message)
        
        # Check for spam
        await self.check_spam(message)

    async def check_filtered_words(self, message: discord.Message):
        """Check if message contains filtered words."""
        filtered_words = await database.get_filter_words(message.guild.id)
        message_content = message.content.lower()
        
        for word_tuple in filtered_words:
            word = word_tuple[0]
            if re.search(r'\b' + re.escape(word) + r'\b', message_content):
                try:
                    await message.delete()
                    embed = discord.Embed(
                        title="Message Deleted",
                        description=f"Your message was deleted because it contains a filtered word.",
                        color=discord.Color.red()
                    )
                    await message.author.send(embed=embed)
                except:
                    pass
                break

    async def check_spam(self, message: discord.Message):
        """Check for spam messages."""
        user_id = message.author.id
        current_time = discord.utils.utcnow().timestamp()
        
        if user_id not in self.spam_cache:
            self.spam_cache[user_id] = []
        
        # Remove old timestamps
        self.spam_cache[user_id] = [
            ts for ts in self.spam_cache[user_id]
            if current_time - ts < self.spam_timeframe
        ]
        
        self.spam_cache[user_id].append(current_time)
        
        # Check if user exceeded spam threshold
        if len(self.spam_cache[user_id]) >= self.spam_threshold:
            try:
                await message.delete()
                await message.author.timeout(
                    discord.utils.utcnow().shift(minutes=5),
                    reason="Spam detected"
                )
                embed = discord.Embed(
                    title="Spam Detected",
                    description="You have been muted for 5 minutes due to spam.",
                    color=discord.Color.red()
                )
                await message.author.send(embed=embed)
                self.spam_cache[user_id] = []
            except:
                pass

    @app_commands.command(name="filter_add", description="Add a word to the filter list")
    @app_commands.describe(word="The word to filter")
    async def filter_add(self, interaction: discord.Interaction, word: str):
        """Add a word to the filter list."""
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You don't have permission to manage filters!", ephemeral=True)
            return

        await database.add_filter_word(interaction.guild_id, word)
        
        embed = discord.Embed(
            title="Filter Added",
            description=f"The word '{word}' has been added to the filter list.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="filter_remove", description="Remove a word from the filter list")
    @app_commands.describe(word="The word to remove from the filter")
    async def filter_remove(self, interaction: discord.Interaction, word: str):
        """Remove a word from the filter list."""
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You don't have permission to manage filters!", ephemeral=True)
            return

        await database.remove_filter_word(interaction.guild_id, word)
        
        embed = discord.Embed(
            title="Filter Removed",
            description=f"The word '{word}' has been removed from the filter list.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="filters", description="View all filtered words")
    async def view_filters(self, interaction: discord.Interaction):
        """View all filtered words for the guild."""
        filtered_words = await database.get_filter_words(interaction.guild_id)
        
        if not filtered_words:
            await interaction.response.send_message("No filtered words set for this server.", ephemeral=True)
            return

        words_list = "\n".join([word[0] for word in filtered_words])
        
        embed = discord.Embed(
            title="Filtered Words",
            description=words_list,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Total: {len(filtered_words)}")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(MessageModeration(bot))