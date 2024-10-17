import requests
import json

def get_api_data(rodada):
    uri = f'https://api.football-data.org/v4/competitions/BSA/matches?matchday={rodada}'
    headers = { 'X-Auth-Token': '77e912143e55450cab5e22d0ff600fd9' }

    response = requests.get(uri, headers=headers)
    if response.status_code == 200:
        dados = response.json()
        return dados
    else:
        print("Não foi possivel conectar a API")
