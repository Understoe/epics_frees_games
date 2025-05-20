import discord
import requests
import os
import asyncio
from datetime import datetime

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
ROLE_NAME = os.getenv("DISCORD_ROLE_NAME", "EpicGamesFans")

async def get_free_games():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=fr"
    response = requests.get(url)
    data = response.json()
    games = []

    elements = data['data']['Catalog']['searchStore']['elements']
    for game in elements:
        if game.get("promotions") and game["promotions"].get("promotionalOffers"):
            title = game['title']
            end_date = game["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"]
            end_date = datetime.fromisoformat(end_date[:-1]).strftime("%d %B %Y")
            games.append((title, end_date))

    return games

async def send_discord_message():
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = client.get_channel(CHANNEL_ID)
        guild = channel.guild
        role = discord.utils.get(guild.roles, name=ROLE_NAME)

        games = await get_free_games()
        if not games:
            message = "Aucun jeu gratuit cette semaine. 😢"
        else:
            message = f"🎮 **Jeux gratuits sur l'Epic Games Store cette semaine !**\n\n"
            for title, end in games:
                message += f"- 🆓 *{title}* (jusqu'au {end})\n"
            message += f"\n{role.mention} foncez les récupérer ! 🔥"

        await channel.send(message)
        await client.close()

    await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(send_discord_message())
