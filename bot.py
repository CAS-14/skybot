import discord
from discord.ext import commands
import dotenv
import os
import aiohttp
import random

dotenv.load_dotenv()
TOKEN = os.getenv("SKYBOT_TOKEN")

class MyBot(commands.Bot):
    def __init__(self, *, intents: discord.Intents = discord.Intents.default()):
        super().__init__(
            intents=intents,
            command_prefix="s!",
            owner_id=415616777356312576
        )

    async def setup_hook(self) -> None:
        async for guild in self.fetch_guilds():
            print(f"Registering commands for {guild}")
            self.tree.copy_global_to(guild=guild)
        await self.tree.sync()

bot = MyBot(intents=discord.Intents.default())

async def get_image(tags: str, page_max: int = 1):
    page = random.randint(1, page_max)
    url = f"https://konachan.net/post.json?page={page}&tags={tags}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = await response.json()

        for post in result:
            if post["rating"] != "s":
                result.remove(post)

        image_url = random.choice(result)["file_url"]
        return image_url
    
    except Exception as e:
        return f"Sorry, something went wrong. Tell weirdcease: `{e}`"

@bot.tree.command(name="hello", description="Test command which says hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi Sky!")

# @bot.tree.command(name="image", description="Sends a random image from konachan.net based on the tags given.")
# async def image(interaction: discord.Interaction, )

@bot.tree.command(name="konata", description="Sends a random Konata Izumi image.")
async def konata(interaction: discord.Interaction):
    image_url = await get_image("izumi_konata", 29)
    await interaction.response.send_message(image_url)
    
@bot.tree.command(name="miku", description="Sends a random Hatsune Miku image.")
async def miku(interaction: discord.Interaction):
    image_url = await get_image("hatsune_miku", 652)
    await interaction.response.send_message(image_url)

bot.run(TOKEN)
