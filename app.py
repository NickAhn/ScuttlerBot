import discord
import secret
import motor.motor_asyncio
import riot

TOKEN = secret.disc_token

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("{0.user} is Online.".format(client))

@client.event
async def on_disconnect():
    print("{} has been disconnected.".format(client))


@client.event
async def on_message(message):
    '''
    This function handles ScuttlerBot's commands.
    '''
    username = str(message.author).split('#')[0]
    channel = str(message.channel.name)
    user_message = str(message.content).split(" ")
    print(f"{username}: {user_message} ({channel})")

    if message.author == client:
        return

    ## -- Bot Commands -- ##
    if user_message[0] == "~hello":
        await message.channel.send(f"Hello {username}!")
        return

    if user_message[0] == "~leaguerank":
        await message.channel.send("~leaguerank called")

    if user_message[0] == "~leaguestats":
        '''
        Get complete information about Summoner's stats
        Usage: ~leaguestats <summonerName>
        '''
        if len(user_message) == 1:
            await message.channel.send('Please enter:"~leaguestats [Summoner Name]"')
            return
        
        
        info = riot.getAccountById(user_message[1])
        summonerData = riot.getSummonerDataByEncryptedId(info['id'])
        summonerName = "**" + user_message[1] + "**\n"
        rank = "**" + summonerData[0]['tier'].capitalize() + " " + summonerData[0]['rank'] + "**"
        await message.channel.send(summonerName + rank) 
        return


# async def main():
if __name__ == "__main__":
    client.run(TOKEN)
    # async with client:
        # client.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient("URI")
        # await client.start(TOKEN) #.start() is a coroutine

