import discord
import secret

TOKEN = secret.disc_token

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("{0.user} is Online".format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} ({channel})")

    if message.author == client:
        return

    if user_message.lower() == "test":
        await message.channel.send(f"Hello {username}!")
        return

if __name__ == '__main__':
    client.run(TOKEN)

