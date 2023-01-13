# Riot API handler
import requests
from pprint import pprint
import secret

api_key = secret.api_key

# Header required for all API calls
HEADER = {
    "X-Riot-Token": api_key
}


def getAccountById(summonerName: str) -> dict:
    '''
    Get Account info by Summoner Name
    * Params:
        summonerName: str  = In Game Name
    * Return: dictionary with the following keys:
        accountId: str      = Encrypted account ID. Max length 56 characters.
        profileIconId: int	= ID of the summoner icon associated with the summoner.
        revisionDate: long  = Date summoner was last modified specified as epoch milliseconds. The following events will update this timestamp: summoner name change, summoner level change, or profile icon change.
        name:str	        = Summoner name.
        id:str          	= Encrypted summoner ID. Max length 63 characters.
        puuid:str	        = Encrypted PUUID. Exact length of 78 characters.
        summonerLevel:long	= Summoner level associated with the summoner.
    '''
    endpoint = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}'
    res = requests.get(endpoint, headers=HEADER)
    json_data = res.json()
    print(json_data)
    return json_data

# TODO: check if data for SOLO_QUEUE_5x5 or FLEX exist
def getSummonerDataByEncryptedId(encryptedSummonerId: str) -> dict:
    '''
    Get Detailed Summoner Data for Ranked Flex and Solo/Duo.
    * Params:
        encryptedSummonerId: str    = 'id' value from getAccountById
    * Return:
        json as dictionary with data such as Rank, Tier, Wins, Losses, etc...
    '''
    endpoint = f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{encryptedSummonerId}'
    endpoint += "?api_key=" + api_key
    res = requests.get(endpoint)
    print(res)
    return res.json()

