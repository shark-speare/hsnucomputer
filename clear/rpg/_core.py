import json
import random

class AllPlayerData:
    def __init__(self) -> None:
        self.data = open('rpgdata/playerData.json', mode='r+', encoding='utf8')
        self.json_data = json.load(self.data)

    def read(self, keys: list):
        data_:dict = self.json_data
        if keys:
            for key in keys:
                data_ = data_.get(key, {})
        return data_

    def write(self, keys: list, value: dict):
        index_ = ''
        for i in range(len(keys)):
            index_ += f'["{keys[i]}"]'
        exec(f'self.json_data{index_} = value')
        self.data.seek(0)
        self.data.truncate()
        json.dump(self.json_data, self.data, ensure_ascii=False, indent=4)

    def close(self):
        self.data.close()

    def __del__(self):
        self.close()

class Book:
    def __init__(self, book_id):
        with open('rpgdata/books.json', mode='r', encoding='utf8') as file:
            books:dict = json.load(file)
            book_data = books[book_id]
        self.title = book_data['title']
        self.author = book_data['author']
        self.year = book_data['year']
        self.path = book_data['path']
        with open(self.path, mode='r', encoding='utf8') as file:
            self.content = file.read()

    def read(self):
        return f'## 《{self.title}》\n{self.content}'
    
    def __call__(self):
        return self.read()
    
class Item:
    def __init__(self, item_id):
        with open('rpgdata/items.json', mode='r', encoding='utf8') as file:
            items:dict = json.load(file)
            item_data:dict = items.get(item_id, {})
        self.id = item_data.get('id')
        self.name = item_data.get('name')
        self.description = item_data.get('description')

    def is_in_bag(self, player_id) -> bool:
        player_json_data = AllPlayerData().read([player_id])
        return self.id in player_json_data['bag']['items'].keys() and player_json_data['bag']['items'][self.id] > 0
    
class Work:
    def __init__(self, work_id):
        with open('rpgdata/works.json', mode='r', encoding='utf8') as file:
            works:dict = json.load(file)
            self.data:dict = works.get(work_id, {})

        self.id = self.data.get('id')
        self.name = self.data.get('name')
        self.description = self.data.get('description')
        self.reward = self.data.get('reward')
        self.time = self.data.get('time')
        self.overTimeRewardRatio = self.data.get('overTimeRewardRatio')
        self.drops = self.data.get('drops')
        self.usableItems = self.data.get('usableItems')

    def get_reward(self):
        return random.randint(self.reward[0], self.reward[1])
    
    def get_additional_reward(self, usedItems:list):
        additional_reward = 0
        for usedItem in usedItems:
            item_setting = self.usableItems[usedItem]
            additional_reward += random.randint(item_setting['reward'][0], item_setting['reward'][1])
        return additional_reward
    
    def get_drops(self, usedItems:list):
        drops = {}
        drops_tables = [self.drops]
        for usedItem in usedItems:
            drops_tables.append(self.usableItems[usedItem]['drops'])
        for drops_table in drops_tables:
            for drop_item_id in drops_table.keys():
                drop = drops_table[drop_item_id]
                if random.random() < drop['probability']:
                    amount = random.randint(drop['amount'][0], drop['amount'][1])
                    if amount:
                        drops[drop_item_id] = amount
        return drops


class Player:
    def __init__(self, player_id):
        self.id = player_id

        all_player_json_data = AllPlayerData().json_data

        if player_id not in all_player_json_data.keys():
            self.create()
            all_player_json_data = AllPlayerData().json_data

        player_data = all_player_json_data[player_id]

        self.status = player_data.get('status')
        self.asset = player_data.get('asset')
        self.bag = player_data.get('bag')

        for physical_attack_id in player_data.get('physicalAttacks', []):
            setattr(self, physical_attack_id, PhysicalAttack(self, physical_attack_id))

    def create(self):
        with open('rpgdata/template.json', mode='r', encoding='utf8') as file:
            player_json_data_template:dict = json.load(file)
        all_player_data = AllPlayerData()
        all_player_json_data = all_player_data.json_data
        all_player_json_data[self.id] = player_json_data_template
        all_player_data.write([], all_player_json_data)
        all_player_data.close()

    def work(self, work: Work, usedItems:list) -> str:
        """
        will output a string to show the result of the work
        """
        from datetime import datetime as dt
        from datetime import timezone, timedelta

        startTimestamp = dt.now(tz=timezone(timedelta(hours=8))).isoformat()

        all_player_data = AllPlayerData()
        player_doing_data = all_player_data.read([self.id, 'status', 'doing'])

        if player_doing_data.get('id'):
            return f'你正在{Work(player_doing_data.get("id")).name}，分身乏術'
        if not work.id:
            return '工作不存在，天下沒有白吃的午餐，也沒有白做的工作！'
        for usedItem in usedItems:
            if usedItem:
                usedItem_object = Item(usedItem)
                if not usedItem_object.is_in_bag(self.id):
                    return f'你沒有{usedItem_object.name}'
                elif usedItem not in work.usableItems:
                    return f'這個工作不需要{usedItem_object.name}'
                else:
                    player_doing_data['usedItems'].append(usedItem)

        player_doing_data['startTimestamp'] = startTimestamp
        player_doing_data['id'] = work.id
        all_player_data.write([self.id, 'status', 'doing'], player_doing_data)
        all_player_data.close()
        return f'開始{work.name}\n請準時完成工作並回報進度！'

    def finish_work(self):
        from datetime import datetime as dt
        from datetime import timezone, timedelta

        now = dt.now(tz=timezone(timedelta(hours=8)))

        all_player_data = AllPlayerData()
        player_json_data = all_player_data.read([self.id])
        player_doing_data = player_json_data['status']['doing']
        work = Work(player_doing_data.get('id'))

        if not work.id:
            return '你沒有在工作'
        working = (now - dt.fromisoformat(player_doing_data['startTimestamp'])).seconds
        if working < work.time[0]:
            return '工作時長不足'
        
        money = work.get_reward()
        if working <= work.time[1]:
            work_compelete_message = '完美工作！雇主很滿意 :)\n'
        else:
            work_compelete_message = '工作超時！你很累，雇主不開心 :(\n'
            money *= work.overTimeRewardRatio
            money = int(money)
        work_compelete_message += f'你獲得了 {money}！\n'

        drops = work.get_drops(player_doing_data['usedItems'])
        for drop_item_id in drops.keys():
            drop_item = Item(drop_item_id)
            work_compelete_message += f'你意外的獲得了 {drops[drop_item_id]} 個 {drop_item.name}！\n'
            player_json_data['bag']['items'][drop_item_id] = player_json_data['bag']['items'].get(drop_item_id, 0) + drops[drop_item_id]

        additional_reward = work.get_additional_reward(player_doing_data['usedItems'])
        if additional_reward:
            work_compelete_message += f'帶來了額外的 {additional_reward}！\n'
            money += additional_reward

        for usedItem in player_doing_data['usedItems']:
            item_setting = work.usableItems[usedItem]
            if random.random() <= item_setting['disappear_probability']:
                player_json_data['bag']['items'][usedItem] -= 1
                if player_json_data['bag']['items'][usedItem] == 0:
                    player_json_data['bag']['items'].pop(usedItem)
                work_compelete_message += f'{Item(usedItem).name} 消耗殆盡\n'

        player_json_data['status']['doing']['id'] = ""
        player_json_data['status']['doing']['startTimestamp'] = ""
        player_json_data['status']['doing']['usedItems'] = []
        player_json_data['asset']['money'] += money
        all_player_data.write([self.id], player_json_data)
        all_player_data.close()

        return work_compelete_message
    

class PhysicalAttack:
    def __init__(self, user, attack_id):
        self.user = user

        with open('rpgdata/physicalAttacks.json', mode='r', encoding='utf8') as file:
            attacks:dict = json.load(file)
            attack_data:dict = attacks.get(attack_id, {})
        self.id = attack_data.get('id')
        self.name = attack_data.get('name')
        self.description = attack_data.get('description')
        self.damage:str = attack_data.get('damage')

    def attack(self, target):
        damage = eval(self.damage.format(ATK=self.user.ATK, STR=self.user.STR, DEF_=target.DEF))
        if random.random() < self.user.CRI: damage *= 2
        target.HP -= damage
        return damage

class Enemy:
    def __init__(self, enemy_id):
        with open('rpgdata/enemies.json', mode='r', encoding='utf8') as file:
            enemies:dict = json.load(file)
            enemy_data:dict = enemies.get(enemy_id, {})
        self.id = enemy_data.get('id')
        self.name = enemy_data.get('name')

        self.HP = enemy_data.get('HP')
        self.MP = enemy_data.get('MP')
        self.ATK = enemy_data.get('ATK')
        self.CRI = enemy_data.get('CRI')
        self.DEF = enemy_data.get('DEF')
        self.STR = enemy_data.get('STR')
        self.SPD = enemy_data.get('SPD')
        self.AGI = enemy_data.get('AGI')
        self.CON = enemy_data.get('CON')
        self.MEN = enemy_data.get('MEN')
        self.LUK = enemy_data.get('LUK')

        for physical_attack_id in enemy_data.get('physicalAttacks', []):
            setattr(self, physical_attack_id, PhysicalAttack(self, physical_attack_id))

        self.reward = enemy_data.get('reward')
        self.drops = enemy_data.get('drops')