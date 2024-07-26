import requests
from bs4 import BeautifulSoup
import json

# 初始化一个空字典，用于存储所有卡片的信息
all_cards = {}
all_types = ["suit-of-swords","suit-of-cups","suit-of-wands","suit-of-pentacles","major-arcana"]

num_cards_starts = 1
num_cards_max = 15
# 遍历多个页面
for cardtype in all_types:
    if cardtype == "major-arcana":
        num_cards_starts = 0
        num_cards_max = 22
    for num in range(num_cards_starts,num_cards_max):  # 假设页面范围为1到22，根据实际情况调整
        url = f"https://www.tarotchina.net/{cardtype}{num}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 获取卡片名称
        title = soup.title.text
        __ = (title.split("_"))
        card = (__[1])[:-2]
        all_cards[card] = {}
        print(f"card:{card}")

        # 获取所有表格内容
        tables = soup.find_all('table')

        # 根据表格数量的不同，解析不同位置的信息
        if len(tables) >= 3:
            # 第二个表格作为正位信息
            table2 = tables[1]
            symbol_rows = table2.find_all('tr')
            positive_meaning = {}
            for row in symbol_rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    symbol = cells[0].text.strip()
                    interpretation = cells[1].text.strip()
                    positive_meaning[symbol] = interpretation
            all_cards[card]["正位"] = positive_meaning

            # 第三个表格作为逆位信息
            table3 = tables[2]
            symbol_rows = table3.find_all('tr')
            reverse_meaning = {}
            for row in symbol_rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    symbol = cells[0].text.strip()
                    interpretation = cells[1].text.strip()
                    reverse_meaning[symbol] = interpretation
            all_cards[card]["逆位"] = reverse_meaning

        elif len(tables) == 2:
            # 第一个表格作为正位信息
            table1 = tables[0]
            symbol_rows = table1.find_all('tr')
            positive_meaning = {}
            for row in symbol_rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    symbol = cells[0].text.strip()
                    interpretation = cells[1].text.strip()
                    positive_meaning[symbol] = interpretation
            all_cards[card]["正位"] = positive_meaning

            # 第二个表格作为逆位信息
            table2 = tables[1]
            symbol_rows = table2.find_all('tr')
            reverse_meaning = {}
            for row in symbol_rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    symbol = cells[0].text.strip()
                    interpretation = cells[1].text.strip()
                    reverse_meaning[symbol] = interpretation
            all_cards[card]["逆位"] = reverse_meaning

# 将结果写入到 JSON 文件中
with open('cards.json', 'w', encoding='utf-8') as f:
    json.dump(all_cards, f, ensure_ascii=False, indent=4)

print("数据已保存到 cards.json 文件中。")
