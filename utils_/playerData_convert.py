import json
import copy

def playerData_convert():
    with open('rpgdata/playerData.json', encoding='utf8') as file:
        player_json_data = json.load(file)
    with open('rpgdata/template.json', encoding='utf8') as file:
        template = json.load(file)

    for player_id in player_json_data.keys():
        player_data = player_json_data[player_id]
        player_json_data[player_id] = copy.deepcopy(template)  # Create a deep copy of template
        player_json_data[player_id]['status']['doing']['id'] = player_data['status']['doing']
        player_json_data[player_id]['status']['doing']['startTimestamp'] = player_data['status']['workStartTimestamp']
        player_json_data[player_id]['status']['LUK'] = player_data['status']['LUK']
        player_json_data[player_id]['asset']['money'] = player_data['asset']['money']
        player_json_data[player_id]['bag']['items'] = player_data['bag']['items']

    with open('rpgdata/playerData.json', mode='w', encoding='utf8') as file:
        json.dump(player_json_data, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    playerData_convert()
