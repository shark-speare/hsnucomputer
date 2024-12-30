import json




with open('playerData.json',mode='r+',encoding='utf8') as file:
    data:dict = json.load(file)

    for i in data.keys():
        id = data[i]['status']['doing']
        time = data[i]['status']["workStartTimestamp"]
        data[i]['status']['doing'] = {
            "id" : id,
            "useItems" : [],
            "startTimestamp" : time,

        }
    file.seek(0)
    file.truncate()

    json.dump(data,file, ensure_ascii=False, indent=4)