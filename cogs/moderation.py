import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import database

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='warn', description='Warn a user')
    @app_commands.describe(
        user='The user to warn',
        reason='The reason for the warning'
    )
    async def warn(self, interaction: discord.Interaction, user: discord.User, reason: str = None):
        """Warn a user."""
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("You don't have permission to warn users.", ephemeral=True)
            return

        await database.add_warning(user.id, interaction.guild_id, interaction.user.id, reason)
        warnings = await database.get_warnings(user.id, interaction.guild_id)
        
        embed = discord.Embed(
            title='User Warned',
            color=discord.Color.yellow(),
            timestamp=datetime.now()
        )
        embed.add_field(name='User', value=user.mention, inline=False)
        embed.add_field(name='Moderator', value=interaction.user.mention, inline=False)
        embed.add_field(name='Reason', value=reason or 'No reason provided', inline=False)
        embed.add_field(name='Total Warnings', value=len(warnings), inline=False)
        embed.set_footer(text=f'User ID: {user.id}')
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='warnings', description='Check warnings for a user')
    @app_commands.describe(user='The user to check warnings for')
    async def check_warnings(self, interaction: discord.Interaction, user: discord.User):
        """Check warnings for a user."""
        warnings = await database.get_warnings(user.id, interaction.guild_id)
        
        if not warnings:
            await interaction.response.send_message(f'{user.mention} has no warnings.', ephemeral=True)
            return

        embed = discord.Embed(
            title=f'Warnings for {user}',
            color=discord.Color.yellow(),
            description=f'Total warnings: {len(warnings)}'
        )
        
        for idx, warning in enumerate(warnings, 1):
            warning_id, user_id, guild_id, moderator_id, reason, timestamp = warning
            embed.add_field(
                name=f'Warning #{idx}',
                value=f'**Reason:** {reason or 'No reason'}\n**Moderator:** <@{moderator_id}>\n**Date:** {timestamp}',
                inline=False
            )
        
        embed.set_footer(text=f'User ID: {user.id}')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='mute', description='Mute a user')
    @app_commands.describe(
        user='The user to mute',
        duration='Duration in minutes (0 for indefinite)',
        reason='The reason for the mute'
    )
    async def mute(self, interaction: discord.Interaction, user: discord.User, duration: int = 0, reason: str = None):
        """Mute a user."""
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("You don't have permission to mute users.", ephemeral=True)
            return

        guild = interaction.guild
        member = await guild.fetch_member(user.id)
        
        if member is None:
            await interaction.response.send_message("User is not in this server.", ephemeral=True)
            return

        mute_time = None
        if duration > 0:
            mute_time = datetime.now() + timedelta(minutes=duration)
        
        await member.timeout(timedelta(minutes=duration) if duration > 0 else None, reason=reason)
        await database.add_mute(user.id, guild.id, interaction.user.id, reason, mute_time)
        
        duration_text = f'{duration} minutes' if duration > 0 else 'indefinite'
        
        embed = discord.Embed(
            title='User Muted',
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.add_field(name='User', value=user.mention, inline=False)
        embed.add_field(name='Moderator', value=interaction.user.mention, inline=False)
        embed.add_field(name='Duration', value=duration_text, inline=False)
        embed.add_field(name='Reason', value=reason or 'No reason provided', inline=False)
        embed.set_footer(text=f'User ID: {user.id}')
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='unmute', description='Unmute a user')
    @app_commands.describe(user='The user to unmute')
    async def unmute(self, interaction: discord.Interaction, user: discord.User):
        """Unmute a user."""
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("You don't have permission to unmute users.", ephemeral=True)
            return

        guild = interaction.guild
        member = await guild.fetch_member(user.id)
        
        if member is None:
            await interaction.response.send_message("User is not in this server.", ephemeral=True)
            return

        await member.timeout(None)
        await database.remove_mute(user.id, guild.id)
        
        embed = discord.Embed(
            title='User Unmuted',
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.add_field(name='User', value=user.mention, inline=False)
        embed.add_field(name='Moderator', value=interaction.user.mention, inline=False)
        embed.set_footer(text=f'User ID: {user.id}')
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='kick', description='Kick a user from the server')
    @app_commands.describe(
        user='The user to kick',
        reason='The reason for the kick'
    )
    async def kick(self, interaction: discord.Interaction, user: discord.User, reason: str = None):
        """Kick a user from the server."""
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("You don't have permission to kick users.", ephemeral=True)
            return

        guild = interaction.guild
        member = await guild.fetch_member(user.id)
        
        if member is None:
            await interaction.response.send_message("User is not in this server.", ephemeral=True)
            return

        await guild.kick(member, reason=reason)
        
        embed = discord.Embed(
            title='User Kicked',
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        embed.add_field(name='User', value=user.mention, inline=False)
        embed.add_field(name='Moderator', value=interaction.user.mention, inline=False)
        embed.add_field(name='Reason', value=reason or 'No reason provided', inline=False)
        embed.set_footer(text=f'User ID: {user.id}')
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='ban', description='Ban a user from the server')
    @app_commands.describe(
        user='The user to ban',
        reason='The reason for the ban'
    )
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: str = None):
        """Ban a user from the server."""
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("You don't have permission to ban users.", ephemeral=True)
            return

        guild = interaction.guild
        
        try:
            await guild.ban(user, reason=reason)
            await database.add_ban(user.id, guild.id, interaction.user.id, reason)
        except discord.NotFound:
            await interaction.response.send_message("User not found.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title='User Banned',
            color=discord.Color.dark_red(),
            timestamp=datetime.now()
        )
        embed.add_field(name='User', value=user.mention, inline=False)
        embed.add_field(name='Moderator', value=interaction.user.mention, inline=False)
        embed.add_field(name='Reason', value=reason or 'No reason provided', inline=False)
        embed.set_footer(text=f'User ID: {user.id}')
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))