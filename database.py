import aiosqlite
import os
from pathlib import Path

DATABASE_PATH = os.getenv("DATABASE_PATH", "moderation.db")

async def init_db():
    """Initialize the database with required tables."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,
                moderator_id INTEGER NOT NULL,
                reason TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS mutes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,
                moderator_id INTEGER NOT NULL,
                reason TEXT,
                mute_time DATETIME,
                is_active BOOLEAN DEFAULT 1,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,
                moderator_id INTEGER NOT NULL,
                reason TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS message_filters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                word TEXT NOT NULL UNIQUE,
                action TEXT DEFAULT 'delete',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.commit()

async def add_warning(user_id: int, guild_id: int, moderator_id: int, reason: str = None):
    """Add a warning to a user."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO warnings (user_id, guild_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
            (user_id, guild_id, moderator_id, reason)
        )
        await db.commit()

async def get_warnings(user_id: int, guild_id: int):
    """Get all warnings for a user in a guild."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT * FROM warnings WHERE user_id = ? AND guild_id = ?",
            (user_id, guild_id)
        ) as cursor:
            return await cursor.fetchall()

async def add_mute(user_id: int, guild_id: int, moderator_id: int, reason: str = None, mute_time = None):
    """Add a mute record."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO mutes (user_id, guild_id, moderator_id, reason, mute_time) VALUES (?, ?, ?, ?, ?)",
            (user_id, guild_id, moderator_id, reason, mute_time)
        )
        await db.commit()

async def get_mutes(user_id: int, guild_id: int):
    """Get all mutes for a user in a guild."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT * FROM mutes WHERE user_id = ? AND guild_id = ? AND is_active = 1",
            (user_id, guild_id)
        ) as cursor:
            return await cursor.fetchall()

async def remove_mute(user_id: int, guild_id: int):
    """Remove an active mute for a user."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE mutes SET is_active = 0 WHERE user_id = ? AND guild_id = ? AND is_active = 1",
            (user_id, guild_id)
        )
        await db.commit()

async def add_ban(user_id: int, guild_id: int, moderator_id: int, reason: str = None):
    """Add a ban record."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO bans (user_id, guild_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
            (user_id, guild_id, moderator_id, reason)
        )
        await db.commit()

async def add_filter_word(guild_id: int, word: str, action: str = "delete"):
    """Add a filtered word for a guild."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        try:
            await db.execute(
                "INSERT INTO message_filters (guild_id, word, action) VALUES (?, ?, ?)",
                (guild_id, word.lower(), action)
            )
            await db.commit()
        except aiosqlite.IntegrityError:
            pass

async def get_filter_words(guild_id: int):
    """Get all filtered words for a guild."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT word FROM message_filters WHERE guild_id = ?",
            (guild_id,)
        ) as cursor:
            return await cursor.fetchall()

async def remove_filter_word(guild_id: int, word: str):
    """Remove a filtered word from a guild."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "DELETE FROM message_filters WHERE guild_id = ? AND word = ?",
            (guild_id, word.lower())
        )
        await db.commit()