import os
import asyncio
import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID"))
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))
SOURCE_LANG = os.getenv("SOURCE_LANG", "en")
TARGET_LANG = os.getenv("TARGET_LANG", "ru")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set in .env")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def has_latin(text: str) -> bool:
    return any('a' <= c.lower() <= 'z' for c in text)


def has_cyrillic(text: str) -> bool:
    return any('а' <= c.lower() <= 'я' or c.lower() == 'ё' for c in text)


def translate_text(text: str) -> str:
    """Синхронный перевод — вызывать через asyncio.to_thread."""
    translator = GoogleTranslator(source=SOURCE_LANG, target=TARGET_LANG)
    return translator.translate(text)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Watching channel {SOURCE_CHANNEL_ID} -> posting to {TARGET_CHANNEL_ID}")

    channel = bot.get_channel(SOURCE_CHANNEL_ID)
    if channel:
        print(f"Channel name: {channel.name}, Guild: {channel.guild.name}")
        perms = channel.permissions_for(channel.guild.me)
        print(
            f"Bot perms in channel: view={perms.view_channel}, "
            f"send={perms.send_messages}, embed={perms.embed_links}, "
            f"history={perms.read_message_history}"
        )
    else:
        print("SOURCE CHANNEL NOT FOUND - bot cannot see it!")

    target = bot.get_channel(TARGET_CHANNEL_ID)
    if target is None:
        print("TARGET CHANNEL NOT FOUND - bot cannot see it!")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.channel.id != SOURCE_CHANNEL_ID:
        return
    if not message.content.strip():
        return

    # Команды обрабатываем всегда, даже если сообщение не для перевода
    await bot.process_commands(message)

    text = message.content
    # Переводим только латиницу без кириллицы
    if not has_latin(text) or has_cyrillic(text):
        return

    try:
        translated = await asyncio.to_thread(translate_text, text)
    except Exception as e:
        print(f"Translate error: {e}")
        return

    if not translated or translated == text:
        return

    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if target_channel is None:
        print(f"Target channel {TARGET_CHANNEL_ID} not found")
        return

    embed = discord.Embed(description=translated, color=0x00FF00)
    embed.set_author(
        name=f"{message.author.display_name} (перевод)",
        icon_url=message.author.display_avatar.url,
    )

    try:
        await target_channel.send(embed=embed)
    except Exception as e:
        print(f"Send error: {e}")


if __name__ == "__main__":
    bot.run(TOKEN)
