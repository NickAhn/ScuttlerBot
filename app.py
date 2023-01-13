import discord
import secret
import motor.motor_asyncio
import riot
from pprint import pprint

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


def get_queue_embed_val(summonerData: str, queueType: str) -> str:
    '''
    Helper Function to get value for 'queueType' field for command ```~leaguerank```
    * Params:
      summonerData: str = dictionary returned from riot.getSummonerDataByEncryptionId()
      queueType: str = RANKED_SOLO_5x5 or (ranked flex)
    '''
    q_value = ""
    if not any(dic['queueType'] == queueType for dic in summonerData):
        q_value = "N/A"
    else:
        rank: str = "**{tier} {rank}**".format(
            tier=summonerData[0]['tier'].capitalize(),
            rank=summonerData[0]['rank'])
        winrate: float = (summonerData[0]['wins']/(summonerData[0]['wins'] + summonerData[0]['losses']))*100
        winrate_str: str = "Winrate: **{winrate:.2f}%** ({wins}W / {losses}L)".format(
            winrate=winrate, wins=summonerData[0]['wins'],
            losses=summonerData[0]['losses'])
        q_value = rank + "\n" + winrate_str

    return q_value

# TODO: refactor individual commands to its own command functions
@client.event
async def on_message(message):
    '''
    This function handles ScuttlerBot's commands.
    '''
    username = str(message.author).split('#')[0]
    channel = str(message.channel.name)
    user_message = str(message.content).split(" ")
    print(f"{username}: {user_message} ({channel})")

    if message.author == client.user:
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
        Usage: ~leaguestats <summonerName> (note: summonerName is not case-sensitive)
        '''
        if len(user_message) == 1:
            await message.channel.send('Please enter:"~leaguestats [Summoner Name]"')
            return
        
        info = riot.getAccountById(user_message[1])
        summonerData = riot.getSummonerDataByEncryptedId(info['id'])

        embed = discord.Embed(
            title=info['name'],
        )

        # SOLOQ field
        soloq_value = get_queue_embed_val(summonerData=summonerData, queueType="RANKED_SOLO_5x5")
        embed.add_field(
            name = "Solo/Duo",
            value = soloq_value,
            inline = True)
        
        # FLEXQ field
        flexq_value = get_queue_embed_val(summonerData=summonerData, queueType="FLEX")
        embed.add_field(
            name = "Flex",
            value = flexq_value,
            inline = True)

        # Recent matches field
        # TODO: refactor
        match_value = ''
        matches_puuid = riot.getMatchesByPuuid(puuid=info['puuid'], count=5)
        role_map = {
            'TOP': 'Top',
            'JUNGLE': 'Jng',
            'MIDDLE': 'Mid',
            'BOTTOM': 'Adc',
            'UTILITY':'Sup'
        }
        for match in matches_puuid:
            match_data = riot.getMatchByMatchId(match)
            i = match_data['metadata']['participants'].index(info['puuid'])
            player = match_data['info']['participants'][i]
            k, d, a = player['kills'], player['deaths'], player['assists']
            kda_ratio = (k+a)/d
            msg = '{championName}  ({position})  |  {K}/{D}/{A} ({kda:.2f} KDA)\n'.format(
                championName=player['championName'],
                position = role_map[player['individualPosition']],
                K = k,
                D = d,
                A = a,
                kda = kda_ratio
            )
            match_value += msg
        embed.add_field(
            name = 'Recent Matches',
            value = match_value,
            inline=False
        )

        await message.channel.send(embed=embed)
        return

# async def main():
if __name__ == "__main__":
    client.run(TOKEN)
    # async with client:
        # client.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient("URI")
        # await client.start(TOKEN) #.start() is a coroutine
