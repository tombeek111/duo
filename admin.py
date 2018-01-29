from game import game
from user import User
from config import config
import sys

args = sys.argv

    
    
game.create_objects()

controller = game.controller
controller.init()


user1 = User()
user1.name = 'Tom'
user1.telegram_id = config['user1_id']
user1.link = 'https://www.duolingo.com/2017-06-30/users/42447025?fields=courses'
user1.language = 'DUOLINGO_UK_EN'
game.user_manager.add_user(user1)

user2 = User()
user2.name = 'Ananas'
user2.link = 'https://www.duolingo.com/2017-06-30/users?username=Anastasia130'
user2.language = 'DUOLINGO_NL-NL_EN'
game.user_manager.add_user(user2)

#user1.duolingo_xp = 0
#user2.duolingo_xp = 1
#checker = DuolingoChecker([user1,user2])
#ans = checker.check()
#print(ans)
#

controller.chat_id = config['chat_id']
game.load_game(True)

if '-status' in args:
    print('pet health',game.pet.health)
    print('sleep',game.pet.sleeping)
    print('ananas duo xp',game.user_manager.users[1].duolingo_xp)
    print('ananas money',game.user_manager.users[1].money)
	
	
if '-sub_duo' in args:
    game.user_manager.users[1].duolingo_xp -= 10
    print('substracted 10 xp')
	
if '-remove_money' in args:
	game.user_manager.users[1].money -= 900
	print('removed money')

if '-reset_duo' in args:
    game.user_manager.users[1].link = 'https://www.duolingo.com/2017-06-30/users?username=Anastasia130'
    game.user_manager.users[1].init_duolingo_xp()
    print('duolingo reset')
game.save_game()
print('game saved')
"""
pet = Pet()
pet.name = 'flaf'

controller.pet = pet
pet.c = controller

controller.init()
#controller.offline_listener()
"""
# -*- coding: utf-8 -*-

