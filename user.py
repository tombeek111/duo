import requests
from game import game

class User:
    def __init__(self):
        self.items = {}
        self.item_qty = {}
        self.money = game.settings.get_setting(['initial_money'])
        self.link = 'https://www.duolingo.com/2017-06-30/users/42447025?fields=courses'
        self.language = 'DUOLINGO_UK_EN'
        self.duolingo_xp = None
        self.id = None
        self.telegram_id = None
        
    def add_item(self,item):
        if item.name not in self.items:
            self.items[item.name] = item
        
        if item.name not in self.item_qty:
            self.item_qty[item.name] = 0
        self.item_qty[item.name] += 1
        
    def remove_item(self,item):
        self.item_qty[item.name] = max(0,self.item_qty[item.name]-1)
                    
        
    def get_duolingo_xp(self):
        try:
            r = requests.get(self.link)
            found = False
            if r.status_code == 200:
                data = r.json()
                if 'courses' in data:
                    for course in data['courses']:
                        if course['id'] == self.language:
                            found = True
                            xp = course['xp']
        except Exception:
            found = False
        if found:
            return xp
        else:
            return None
        
    def init_duolingo_xp(self):
        self.duolingo_xp = self.get_duolingo_xp()
            
        