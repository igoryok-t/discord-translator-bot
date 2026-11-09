import os
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

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)
translator = GoogleTranslator(source=SOURCE_LANG, target=TARGET_LANG)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Watching channel {SOURCE_CHANNEL_ID} -> posting to {TARGET_CHANNEL_ID}")
    
    channel = bot.get_channel(SOURCE_CHANNEL_ID)
    print(f"Channel object: {channel}")
    if channel:
        print(f"Channel name: {channel.name}, Guild: {channel.guild.name}")
        perms = channel.permissions_for(channel.guild.me)
        print(f"Bot perms in channel: view={perms.view_channel}, send={perms.send_messages}, embed={perms.embed_links}, history={perms.read_message_history}")
    else:
        print("CHANNEL NOT FOUND - bot cannot see it!")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    print(f"MSG from {message.author} in #{message.channel} (id={message.channel.id}): {message.content[:50]}")
    
    if message.channel.id != SOURCE_CHANNEL_ID:
        return
    if not message.content.strip():
        return

    text = message.content
    has_latin = any('a' <= c.lower() <= 'z' for c in text)
    has_cyrillic = any('а' <= c.lower() <= 'я' for c in text)
    if not has_latin or has_cyrillic:
        return

    try:
        translated = translator.translate(text)
        if translated and translated != text:
            embed = discord.Embed(description=translated, color=0x00ff00)
            embed.set_author(
                name=f"{message.author.display_name} (перевод)",
                icon_url=message.author.display_avatar.url
            )
            target_channel = bot.get_channel(TARGET_CHANNEL_ID)
            if target_channel:
                await target_channel.send(embed=embed)
            else:
                print(f"Target channel {TARGET_CHANNEL_ID} not found")
    except Exception as e:
        print(f"Translate error: {e}")

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
