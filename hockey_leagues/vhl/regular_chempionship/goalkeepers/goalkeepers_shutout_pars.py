import json
import sqlite3
import requests
from bs4 import BeautifulSoup

URL = ['http://www.vhlru.ru/stats/leaders/872/so/' ]
#JSONS = ['vhl_winning_goals.json' ]
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.63 Safari/537.36','accept': '*/*'}
c = sqlite3.connect("statistics.sqlite3")

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')

    statistics = soup.find('tbody').find_all('tr')
    #statistics_db = []
    table_name = 'vhl_champ_goalkeepers_shutout'  # это название таблицы, куда пихаем (не бд)
    fields_name = ['place', 'name', 'club','number', 'played_games', 'winnings', 'losing', 'pors', 'safety_factor',
                   'shutout', 'game_time']  # и так далее. Это список самих полей
    fields_string = ", ".join(str(x) for x in fields_name)
    cursor = c.cursor()
    cursor.execute('DELETE FROM ' + table_name)
    for statistic in statistics:
        player = statistic.find_all('td')
        statistics_db = [
            player[0].get_text(),
            player[1].find('a').get_text(),
            player[2].get_text(),
            player[3].get_text(),
            player[4].get_text(),
            player[5].get_text(),
            player[6].get_text(),
            player[7].get_text(),
            player[8].get_text(),
            player[9].get_text(),
            player[10].get_text(),

        ]
        stat_db_string = ", ".join(str(x) for x in statistics_db)  # сделали тоже самое только для списка statistics_db
        string = 'INSERT INTO ' + table_name + '(' + fields_string + ')' + ' VALUES ' + '( ?,?,?,?,?,?,?,?,?,?,? )'
        # склеили строку для SQL запроса
        # string выглядит так: 'INSERT INTO vhl_champ_scorers (list_number, name, club) VALUES (1, Рыжиков Сергей, СКА)
        cursor = c.cursor()

        cursor.execute(string, statistics_db)  # выполняем данный запрос
        # дальше коммитим и закрываем
        c.commit()

    c.close()
    #cursorDB = c.cursor()
    #cursorDB.execute('INSERT INTO statistic.sqlite3 (list_number, name, club, games, pucks, assists, points, plus_minus, winning_pucks, average_time_played) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', statistic.sqlite3)
   # c.commit()


def parse():
    for i in range(len(URL)):
        html = get_html(URL[i])
        if html.status_code == 200:
            get_content(html.text)
        else:
            print("Error, unable to access vhl site")


#t = threading.Timer(86400.0, parse)# раз в день
parse()
#t.start()
