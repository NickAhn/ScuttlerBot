# Riot API handler
import requests
from pprint import pprint
import secret

api_key = secret.api_key

# Header required for all API calls
HEADER = {
    "X-Riot-Token": api_key
}


# API: SUMMONER-V4
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
    return json_data


# API: CHAMPION-MASTERY-V4
def getAllChampionMasteryBySummonerId(summonerId: str) -> list[dict]:
    '''
    Get all champion mastery entries sorted by number of champion points decreasing
    ## Params:
        * summonerId: string = Encripted Summoner Id
    ## Return
        list of dictionaries with all Champion Mastery data sorted by Mastery Points
    '''
    endpoint: str = f'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerId}'
    res = requests.get(endpoint, headers=HEADER)
    return res.json() 


# API: CHAMPION-MASTERY-V4
def getChampionMasteryBySummonerId(summonedId: str, count: int = None) -> list[dict]:
    '''
    Get specified number of champion mastery entries sorted by number of champion points decreasing
    ## Params:
        * summonerId: Encrypted Summoner Id
        * count: Number of entries to retrieve (Default = 3)
    ## Return:
        list of dictionaries with Champion Mastery data sorted by Mastery Points
    '''
    endpoint = f'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonedId}/top'
    params = {}
    if count:
        params['count'] = count
    
    res = requests.get(endpoint, params=params, headers=HEADER)
    return res.json()


# TODO: check if data for SOLO_QUEUE_5x5 or FLEX exist
# API: LEAGUE-V4
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
    json_data = res.json()
    return json_data


# API: MATCH-V5
def getMatchesByPuuid(puuid: str, matchType: str = None, count: int = None) -> list[str]:
    '''
    Get a list of match by puuids
    * Params
        puuid: str
        matchType: str = filter by match type [ranked, normal, tourney, tutorial] [Optional]
        count: int = number of matches to get [Optional]
    '''
    endpoint = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
    params = {}
    if matchType is not None:
        params['type'] = matchType
    if count:
        params['count'] = count
    
    res = requests.get(url=endpoint, params=params, headers=HEADER)
    json_data = res.json()
    return json_data


# API: MATCH-V5
def getMatchByMatchId(puuid: str) -> dict:
    '''
    Get match metadata and info by MatchId (puuid)
    * Params:
        puuid: str = match Id by puuid
    * Return: 
        dictionary metadata and detailed information about match
    '''
    endpoint = f'https://americas.api.riotgames.com/lol/match/v5/matches/{puuid}'
    res = requests.get(url=endpoint, headers=HEADER)
    json_data = res.json()
    return json_data


