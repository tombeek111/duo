import pickle
import os
import random


class Game():
    
    def __init__(self):
        
        self.save_name = 'online_game.pkl'
        self.current_user_id = 0
        self.saving = False
        self.game_stopped = False
        
    def create_objects(self,):
        import pet as _pet
        import controller as _controller
        import user_manager as _user_manager
        import scheduler as _scheduler
        import settings as _settings
        
        
        self.pet = _pet.Pet()
        self.controller = _controller.Controller()
        self.user_manager = _user_manager.UserManager()
        self.scheduler = _scheduler.Scheduler()
        self.settings = _settings.Settings()
        
    
    
    def new_game(self):
        """Starts a new game"""
    
        #Get duolingo
        for user in self.user_manager.users:
            user.init_duolingo_xp()
                    
        self.controller.echo('What is it. It seems like an egg...')
        
        choices = ['Fry it!','Throw it against the wall','Put it in a warm blanket']
        
        def handle_response(choice):
            if choice == 0:
                self.controller.echo('Hmmm. That tasted good. It was a little meaty though')
                self.scheduler.create_timed_event(self.settings.get_setting(['time','restart']),self.new_game)
            elif choice == 1:
                self.controller.echo('What is wrong with you...')
                self.scheduler.create_timed_event(self.settings.get_setting(['time','restart']),self.new_game)
            else:
                self.controller.echo('That was nice of you. Come back in some time')
                
                def hatch():
                    self.controller.echo('The egg has hatched. It is some sort of animal!')
                    self.controller.echo('What do you want to name it?')
                    def give_name(data):
                        name = data['msg']
                        self.pet.name = name
                        self.init_pet()
                        
                      
                        self.controller.echo('Thats a bit of a weird name, but alright!')
                        self.controller.echo('You named it {0}'.format(name))
                        self.controller.echo('Type help to find more commands')
                        self.pet.mood_alert()
                        
                    self.controller.request_input(give_name)
                self.scheduler.create_timed_event(self.settings.get_setting(['time','hatching']),hatch)
                            
        self.controller.request_choice('What do you want to do with it?',choices,handle_response,current_user = False,add_cancel = False) 

  

    
    def init_pet(self):
        """
        Calls functions to init pet
        """
        self.controller.init_pet()
        def hourly_update():
            self.pet.hourly_update()
            self.save_game()
            self.scheduler.create_timed_event(self.settings.get_setting(['time','hourly_update']),hourly_update)
            
        def mood_print():
            
            update_time = round(self.settings.get_setting(['time','mood_print']) * (random.randint(80,120)/100))
            if self.pet.sleeping == 0:
                self.pet.mood_alert()
            self.scheduler.create_timed_event(update_time,mood_print)
        mood_print()
        self.scheduler.create_timed_event(self.settings.get_setting(['time','hourly_update']),hourly_update)
        

        #Start duolingo checker
        import duolingo_checker as _duolingo_checker
        self.duo_checker = _duolingo_checker.DuolingoChecker(self.user_manager.users)
        self.duo_checker.schedule(10)
        
       
    
    def load_game(self,load_only = False):
        name = self.save_name
        print('loading game')
        
        try:
            file = open(name,'rb')
            data = pickle.load(file)
            file.close()
            self.user_manager.users = data['users']
            self.pet = data['pet']
            if self.pet is None or self.pet.alive is False:
                loaded = False
            else:
                loaded = True
        except Exception as e:
            loaded = False
        
        if not load_only:
            if loaded:
                self.init_pet()
                print('game_loaded')
            else:
                self.new_game()
                print('new game')
        
    
    def save_game(self):
        name = self.save_name
        if self.saving == False:
            try:
                self.saving = True
                data = {'users' : self.user_manager.users,'pet' : self.pet}
                tempname = '{0}-tmp'.format(name)
                tempfile  = open(tempname,'wb')
                pickle.dump(data,tempfile)
                tempfile.close()
                os.replace(tempname,name)
                self.saving = False
            except Exception as e:
                print('error while saving')
                print(e)
                
    def end_game(self):
        self.scheduler.stop()
        self.controller.updater.stop()
        self.game_stopped = True
        print('end game')
    

#Create global game
game = Game()