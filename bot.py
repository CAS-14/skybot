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

intents = discord.Intents.default()

bot = MyBot(intents=intents)

# bot.add_cog(Miscellaneous(bot))

@bot.tree.command(name="hello", description="Test command which says hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello there!")

@bot.tree.command(name="konata", description="Sends a random konata image.")
async def konata(interaction: discord.Interaction):
    page = random.randint(1, 29)
    url = f"https://konachan.net/post.json?page={page}&tags=izumi_konata"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = await response.json()

        for post in result:
            if post["rating"] != "s":
                result.remove(post)

        image_url = random.choice(result)["file_url"]
        await interaction.response.send_message(image_url)
    
    except Exception as e:
        await interaction.response.send_message(f"Sorry, something went wrong. Tell weirdcease#0001: `{e}`")

bot.run(TOKEN)
