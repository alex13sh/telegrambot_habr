import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

class StopGame:
    host = 'https://stopgame.ru'
    url = 'https://stopgame.ru/review/new'
    lastkey = ""
    lastkey_file = ""

    def __init__(self, lastkey_file):
        self.lastkey_file = lastkey_file

        if(os.path.exists(lastkey_file)):
            self.lastkey = open(lastkey_file, 'r').read()
        else:
            f = open(lastkey_file, 'w')
            self.lastkey = self.get_lastkey()
            f.write(self.lastkey)
            f.close()

    def new_games(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        new = []
        items = html.select('.tiles > .items > .item > .article-description > div > a')
            
        print("new_games items:", len(items))
        for i in items:
            key = self.parse_href(i['href'])
            if(self.lastkey < key):
                new.append(i['href'])

        return new

    def game_info(self, uri):
        link = self.host + uri
        r = requests.get(link)
        html = BS(r.content, 'html.parser')

        # parse poster image url
        poster = re.match(r'background-image:\s*url\((.+?)\)', html.select('.image-game-logo > .image')[0]['style'])

        # remove some stuff
        remels = html.select('.article.article-show > *')
        for remel in remels:
            remel.extract()

        # form data
        info = {
            "id": self.parse_href(uri),
            "title": html.select('.article-title > a')[0].text,
            "link": link,
            "image": poster.group(1),
            "score": self.identify_score(html.select('.game-stopgame-score > .score')[0]['class'][1]),
            "excerpt": html.select('.article.article-show')[0].text[0:200] + '...'
        };

        return info

    def download_image(self, url):
        r = requests.get(url, allow_redirects=True)

        a = urlparse(url)
        filename = "./parser/downloads/" + os.path.basename(a.path)
        open(filename, 'wb').write(r.content)

        return filename



    def identify_score(self, score):
        if(score == 'score-1'):
            return "Мусор 👎"
        elif(score == 'score-2'):
            return "Проходняк ✋"
        elif(score == 'score-3'):
            return "Похвально 👍"
        elif(score == 'score-4'):
            return "Изумительно 👌"

    def get_lastkey(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        items = html.select('.tiles > .items > .item > div > div > a')
        return self.parse_href(items[0]['href'])

    def parse_href(self, href):
        result = re.match(r'\/show\/(\d+)', href)
        return result.group(1)

    def update_lastkey(self, new_key):
        self.lastkey = new_key

        with open(self.lastkey_file, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(str(new_key))
            f.truncate()

        return new_key

sg = StopGame('lastkey.txt')

import asyncio
from misc import dp, bot
from handlers.subs import get_users_sub
# проверяем наличие новых игр и делаем рассылки
#@dp.message()
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        print("scheduled")
        # проверяем наличие новых игр
        new_games = sg.new_games()

        if(new_games):
            # если игры есть, переворачиваем список и итерируем
            print("New Game")
            new_games.reverse()
            for ng in new_games:
                # парсим инфу о новой игре
                nfo = sg.game_info(ng)
                print("Game Info:", nfo)
                await asyncio.sleep(2)

                # получаем список подписчиков бота
                subscriptions = get_users_sub("StopGame")
                print("subs:", subscriptions)

                # отправляем всем новость
                with open(sg.download_image(nfo['image']), 'rb') as photo:
                    print("Open Photo")
                    for s in subscriptions:
                        print("Send to user_id:", s)
                        await asyncio.sleep(1)
                        await bot.send_photo(
                            s[0],
                            photo,
                            caption = nfo['title'] + "\n" + "Оценка: " + nfo['score'] + "\n" + nfo['excerpt'] + "\n\n" + nfo['link'],
                            disable_notification = True
                        )
                
                # обновляем ключ
                sg.update_lastkey(nfo['id'])
