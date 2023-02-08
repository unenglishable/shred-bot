import discord
from decouple import config
import surf_report

TOKEN = config('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} ready to shred!')

@client.event
async def on_message(message):
    # do nothing if message is from self
    if message.author == client.user:
        return
    if message.content.startswith('$shred'):
        await message.channel.send('shoots')
    if message.content.startswith('$locations'):
        await message.channel.send(surf_report.get_locations())
    if message.content.startswith('$report'):
        command = message.content.split(" ")
        if len(command) < 2:
            await message.channel.send("Usage: `$report <location>`\nSee `$locations` to view available locations")
            return
        location = command[1]
        await message.channel.send(surf_report.get_report_for_location(location))

client.run(TOKEN)
