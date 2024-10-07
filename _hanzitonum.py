def hanzi2number(hanzis: str) -> int:
    hanzi2number_table = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    units = {'十': 10, '百': 100, '千': 1000}
    suffixes = {'兆': 1000000000000, '億': 100000000, '萬': 10000}
    last_is_number = hanzis[0] == '十'
    last_is_unit = False
    last_unit = None
    for hanzi in hanzis:
        now_is_number = hanzi in hanzi2number_table.keys()
        if hanzi == '零': continue
        if not now_is_number:
            if units.get(last_unit, 10000) <= units.get(hanzi, 0): return
            else: last_unit = hanzi
        if last_is_unit:
            if hanzi in units.keys(): return 
        elif not now_is_number ^ last_is_number: return
        last_is_unit = hanzi in units.keys()
        last_is_number = now_is_number
    # 檢查是否包含非合法字符
    valid_characters = set(hanzi2number_table.keys()) | set(units.keys()) | set(suffixes.keys())
    for hanzi in hanzis:
        if hanzi not in valid_characters:
            raise Exception

    def underThousand2number(hanzis: str) -> int:
        number = 0
        temp = 0
        for hanzi in hanzis:
            if hanzi in hanzi2number_table:
                temp = hanzi2number_table[hanzi]
            elif hanzi in units:
                if not temp: temp = 1
                temp *= units[hanzi]
                number += temp
                temp = 0
        return number + temp

    number = 0
    temp = 0
    for suffix in suffixes:
        if suffix in hanzis:
            temp, hanzis = hanzis.split(suffix)
            temp = underThousand2number(temp) if temp else 1
            number += temp * suffixes[suffix]

    number += underThousand2number(hanzis)

    return number
