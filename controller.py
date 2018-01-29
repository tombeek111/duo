# -*- coding: utf-8 -*-
from telegram.ext import CallbackQueryHandler,Updater,  MessageHandler, Filters
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
import logging
from game import game
from config import config


class Controller:
    """
    Handles input and output
    """
    def __init__(self):
        self.exit_called = False
        self.functions = {}
        self.online = True
        self.unsent_msgs = []
        self.events = []
        
    def init(self):
        """
        Init to avoid circular imports
        """
        
        from commands import Store,Pharmacy,Bag,Vet
        
        store = Store()
        store.c = self
        
        pharmacy = Pharmacy()
        pharmacy.c = self
        
        bag = Bag()
        bag.c = self
        
        vet = Vet()
        vet.c = self

        self.commands = {'shop' : store,'pharmacy' : pharmacy, 'bag' : bag,'vet' : vet}
        self.pet = None
        
        
    def init_pet(self):
        """
        Initialize functions after pet has been creaetd
        """
        
        self.functions = {'_mood' : game.pet.print_mood,
                          'mood' : game.pet.mood,
                          '_update' : game.pet.hourly_update,
                          'pet' : game.pet.pet,
                          }
        
    
        
    def echo(self,msg):
        if self.online:
            try:
                while len(self.unsent_msgs) > 0:
                    self.updater.bot.send_message(self.chat_id,self.unsent_msgs[0])
                    del self.unsent_msgs[0]
                    
                self.updater.bot.send_message(self.chat_id,msg)
            except Exception as e:
                self.unsent_msgs.append(msg)
        else:
            print(msg)
        
    def check_unsent(self):
        try:
            while len(self.unsent_msgs) > 0:
                self.updater.bot.send_message(self.chat_id,self.unsent_msgs[0])
                del self.unsent_msgs[0]
        except Exception as e:
            pass
    
    def handle_input(self,data):
        found_event = False
        for i,event in enumerate(self.events):
            executed = event.check_call(data)
            if executed:
                found_event = True
                del self.events[i]
                break
            
        if not found_event:
            self.default_input_callback(data)

    
    def request_cuser_input(self,proceed_function,choice_only = False):
        """
        Requests input from current user
        
        """
        self.request_user_input(game.user_manager.current_user_id,proceed_function,choice_only = choice_only)
        
        
    def request_user_input(self,user_id,proceed_function,choice_only = False):
        """
        requests input from user
        """
        event = User_event(user_id,proceed_function)
        event.choice_only = True
        self.events.append(event)
        
    def request_input(self,proceed_function,choice_only = False):
        event = Event(proceed_function)
        event.choice_only = choice_only
        self.events.append(event)
    
         

    def default_input_callback(self,data):
        """
        Callback called when there are no events
        """
        command = data['msg']
        if command == 'exit':
            self.call_exit()
        elif command == 'help':
            self.echo(' help : Get help \n ' +
              'shop: Go to the shop \n '+
              'bag: Check your bag \n mood : Check mood \n pet: Pet \n pharmacy: visit pharmacy \n vet : Visit vet \n ')
        elif command in self.commands:
            cmd = self.commands[command]
            self.events = [] #Clear user input events.
            cmd.call()
        elif command in self.functions:
            self.functions[command]()
        elif command == 'mood':
            game.pet.mood()
    
    def clear_user_events(self):
        """
        Clears events from current user
        """
        for i, event in enumerate(self.events):
            if event.user_id == None or event.user_id == game.user_manager.current_user_id:
                del self.events[i]
        
    def online_listener(self):
        #todo: user ids
        logging.basicConfig(format='test %(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

        logger = logging.getLogger(__name__)

        def error(bot, update, error):
            """Log Errors caused by Updates."""
            print('error!')
            logger.warning('test')
           # logger.warning('Update "%s" caused error "%s"', update, error)

        self.online = True
        self.updater = Updater(config['api_key'])
        dp = self.updater.dispatcher
        dp.add_error_handler(error)
        
        
        print('start listening')
        def listen(bot,update):
            """
            Listens for telegram custom message
            """

            user_id = None
            telegram_id = update.message.from_user.id
            for user in game.user_manager.users:
                if telegram_id == user.telegram_id:
                    user_id = user.id
                
            if user_id is None:
                for user in game.user_manager.users:
                    if user.telegram_id is None:
                        user.telegram_id = telegram_id
                        print('registered user ',telegram_id)
                        break
                
            if user_id is not None:
                game.user_manager.current_user_id = user_id
                self.handle_input({'msg' : update.message.text.lower(), 'user_id' : user_id,'type' : 'txt'})    
            game.save_game()
        
        def choice_listen(bot,update):
            """
            Listens for telegram inlinekeyboard response
            """
            answer = update.callback_query.data
            print('choice ',answer)
            self.updater.bot.answerCallbackQuery(update.callback_query.id)
   
            user_id = None
            telegram_id = update.callback_query.from_user.id
            for user in game.user_manager.users:
                if telegram_id == user.telegram_id:
                    user_id = user.id
            if user_id is not None:
                game.user_manager.current_user_id = user_id
                self.handle_input({'msg' : answer, 'user_id' : user_id,'type' : 'choice'})
            game.save_game()
            
            
        dp.add_handler(MessageHandler(Filters.text, listen))
        dp.add_handler(CallbackQueryHandler(choice_listen))
        try:
            self.updater.start_polling(poll_interval = 1.0,timeout=10,clean=True,bootstrap_retries=-1)
        except Exception as e:
            print('network error')
            print(e)
            
        #self.updater.start_polling()
       
    
        
        
        
    
        

    def offline_listener(self):
        #todo: remove go back with first question
        self.online = False
        while True:
#            try:
                command = input('what?')
                user_id = int(command[0])
                msg = command[1:]
                self.handle_input({'msg' : msg, 'user_id' : user_id})
                
                self.save_game('game.pkl')
                
                if self.exit_called:
                    break 
#            except Exception as e:
#                print('unrecognized input')
#                print(e)
#                print(e.__dict__)
            
            
      
        
        
    def call_exit(self):
        self.exit_called = True
       
    
        
    
        
    def change_title(self,title):
        if self.online:
            self.updater.bot.setChatTitle(self.chat_id,title)
        else:
            print('title changed')
        
    def request_choice(self,text,choices,proceed_function,current_user = True,add_cancel = True):
    
        """
        Requests a choice and then calls proceed_function
        """
        if self.online:
            keyboard_a = []
            i = -1
            for i,choice in enumerate(choices):
                keyboard_a.append([InlineKeyboardButton(choice,callback_data=i)])
            
            if add_cancel == True:
                keyboard_a.append([InlineKeyboardButton('Cancel',callback_data=i+1)])
                
            keyboard = InlineKeyboardMarkup(keyboard_a)


            self.updater.bot.send_message(self.chat_id,text,reply_markup=keyboard)
            
            def handle_response(data):
                msg = data['msg']
                if msg.isdigit():
                    ans = int(data['msg'])
                    if ans < 0 or ans >= len(choices):
                        ans = None
                    if ans is not None:
                        proceed_function(ans)
                
                        
                        
            if current_user == True:
                self.request_cuser_input(handle_response,choice_only = True)
            else:
                self.request_input(handle_response,choice_only = True)
        else:
            self.echo(text)
            text = ''
            for i,txt in enumerate(choices):
                text += '%s %s \n' % (i+1,txt)
            text += '0 Go back'
            self.echo(text)
            
            def handle_response(data):
                msg = data['msg']
                if msg.isdigit():
                    ans = int(data['msg'])
                    if ans > 0 and ans <= len(choices)+1:
                        ans = ans-1
                    else:
                        ans = None
                    if ans is not None:
                        proceed_function(ans)
                        
            if current_user == True:
                self.request_cuser_input(handle_response)
            else:
                self.request_input(handle_response)
            
            
    
class Event:
    def check_call(self,data):
        self.function(data)
        if self.is_int:
            return data['msg'].isdigit()
        
        return True
    
    def __init__(self,function):
        self.function = function
        self.event = None
        self.is_int = False
        
        
controller = Controller()

class User_event(Event):
    
    def __init__(self,user_id,function):
        self.user_id = user_id
        self.function = function
        self.choice_only = False #Only responds to calls (only supported online)
        
        
    def check_call(self,data):
        if data['user_id'] == self.user_id:
            if self.choice_only == False or (controller.online == True and self.choice_only == True and data['type'] == 'choice') or controller.online == False:
                self.function(data)
                return True
        return False

           
        