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
online = True
if online:
    
    
    pass
    controller.chat_id = config['chat_id']
    
    
        
    try:
        controller.online_listener()
        if '-sayhi' in args:
            controller.echo('connection successfull')
                
        if '-newgame' in args:
            game.new_game()
        else:
            game.load_game()
        
        
        controller.updater.idle()
        
        
    except KeyboardInterrupt:
        print('keyboard interrupt in run')
        game.end_game()
    except Exception as e:
        print('error in run (prob timeout)')
        print(e)
        game.end_game()
        
else:
    #controller.updater.idle()
#
    
    
    #controller.new_game()
    controller.load_game('game.pkl')
    controller.offline_listener()




#controller.init()



"""
pet = Pet()
pet.name = 'flaf'

controller.pet = pet
pet.c = controller

controller.init()
#controller.offline_listener()
"""
