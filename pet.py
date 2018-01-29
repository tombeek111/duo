# -*- coding: utf-8 -*-
import random
from game import game
from datetime import datetime

class Pet:
    def __init__(self):
        self.health = 100
        self.food = 100
        self.happy = 100
        self.love = [3,3]
        self.bored = {}
        self.medicin_needed = None
        self.status_level = 0
        self.alive = True
        self.sleeping = 0
        
        

        
    def check_wake_up(self):
        if self.sleeping > 0:
            self.wake_up()
            
    def pet(self):
        bored = self.is_bored('pet')
        if bored == 0:
            self.happy += game.settings.get_setting(['pet_score'])
            game.controller.echo('{0} is very happy to be petted'.format(self.name))
        elif bored == 1:
            self.happy += round(game.settings.get_setting(['pet_score'])/2)
            game.controller.echo('{0} accepts your petting'.format(self.name))
        else:
            game.controller.echo('It seems like {0} is more interested in other things now'.format(self.name))
        
        if bored <= 1:
            self.increase_bored('pet',10)
            
    def play(self,score,love=1):
        self.check_wake_up()
        self.happy += score
        self.happy = min(self.happy,100)
        self.love[game.user_manager.current_user_id] += 1
        self.love[game.user_manager.current_user_id] = min(self.love[game.user_manager.current_user_id]+love,100)
        
    def feed(self,score,love=1):
        self.check_wake_up()
        self.food = min(self.food+score,100)
        self.love[game.user_manager.current_user_id] = min(self.love[game.user_manager.current_user_id]+love,100)
        
    def print_mood(self):
        msg = 'Health {0} \n Food {1} \n happy {2}'.format(self.health,self.food,self.happy)
        game.controller.echo(msg)
        
        
    def update_mood(self):
        self.happy -= game.settings.get_setting(['hourly','happy_reduction'])
        self.food -= game.settings.get_setting(['hourly','food_reduction'])
        for name in self.bored:
            self.bored[name] = max(self.bored[name]-game.settings.get_setting(['hourly','bored_reduction']),0)
            
        for name,value in enumerate(self.love):
            self.love[name] = max(self.love[name]-game.settings.get_setting(['hourly','love_reduction']),0)
        
        if random.random() < game.settings.get_setting(['hourly','sickness_chance']):
            
            sickness = [item['name'] for key,item in game.settings.get_setting(['medicin']).items()]
            self.medicin_needed = random.choice(sickness)
            
        
        
        #Go to sleep at certain times
        now = datetime.now()
        if (now.hour >= 10 and now.hour <= 6):
            self.sleep(2)
            
        #Progress sleep
        if self.sleeping == 1:
            self.wake_up()
        else:
            self.sleeping = max(0,self.sleeping-1)
       
    
    def hourly_update(self):
        self.update_mood()
        game.save_game()
        
    def get_status(self):
        return {'health' : self.health,'food' : self.food,'happy' : self.happy}
        
    def sleep(self,amount):
        """
        Sleeps for amount of hourly updates
        """
        if self.sleeping == 0:
            game.controller.echo('{0} is now sleeping'.format(self.name))
        self.sleeping = amount
    
    def wake_up(self):
        
        if self.sleeping > 0:
            game.controller.echo('{0} woke up!'.format(self.name))
        self.sleeping = 0
        
    def mood_alert(self):
        #Print message
        lowest_status = min(self.get_status(), key = self.get_status().get)
        print(self.get_status())
        lowest_value = self.get_status()[lowest_status]
        
        msgs = []
        if lowest_value <= 0:
            if self.health <= 0:
                new_title = '(x-x)'
                msgs.append('{0} has died after being very sick :('.format(self.name))
            if self.happy <= 0:
                new_title = '...'
                msgs.append('{0} has ran away'.format(self.name))
            if self.food <= 0:
                new_title = '(x-x)'
                msgs.append('{0} has starved'.format(self.name))
            self.pet_die(random.choice(msgs))
                
        elif lowest_value <= 15:
            if self.health < 15:
                new_title = '(>o<)'
                msgs.append('{0} just threw up, he is looking very unhealthy]'.format(self.name))
                msgs.append('{0} is looking extremely sick'.format(self.name))
            if self.happy <= 15:
                new_title = '.·´¯`(>▂<)´¯`·.'
                msgs.append('{0} is an emotional creature. Someone should give him attention'.format(self.name))
                msgs.append('{0} makes a very sad sound, it seems like he wants to run away'.format(self.name))
                msgs.append('{0} is looking at the door. It seems like he doesnt want to be here'.format(self.name))
            if self.food <= 15:
                new_title = '(x ۝ <)'
                msgs.append('{0} has not eaten in quite some time. He looks very unhealthy'.format(self.name))
                msgs.append('{0} is looking quite starved'.format(self.name))
                
        elif lowest_value <= 40:
            if self.food <= 40:
                new_title = '(° ۝ °)'
                msgs.append('{0} is eating some garbage. It looks disgusting but he is hungry'.format(self.name))
                msgs.append('{0} did not have food for quite some time, he is looking a bit thin'.format(self.name))
                msgs.append('It looks like {0} is not getting enough food'.format(self.name))
                msgs.append(''.format(self.name))
                
                
            if self.happy <= 40:
                new_title = '(◕︵◕)'
                msgs.append('A sad noise comes from {0}'.format(self.name))
                msgs.append('{0} just peed on {1}. Maybe someone should give him attention'.format(self.name,random.choice(game.user_manager.users).name))
                msgs.append('{0} is looking very sad'.format(self.name))
            if self.health <= 40:
                new_title = '(@-@)'
                msgs.append('{0} is looking really sick'.format(self.name))
                msgs.append('{0} does not look healthy'.format(self.name))
                msgs.append('{0} threy up a little.'.format(self.name))
                        
        elif lowest_value <= 60:
            if self.food <= 60:
                new_title = 'ಠ╭╮ಠ'
                
                msgs.append('Feed me! - {0}'.format(self.name))
                msgs.append('{0} has a sensitive stomach, you should probably feed him'.format(self.name))
                msgs.append('{0} tries to steal some food out of the closet. He fails and looks angry'.format(self.name))
            if self.health <= 60:
                new_title = '(๑•﹏•)'
                msgs.append('{0} is drooling quite much, he seems a bit sick'.format(self.name))
                msgs.append('Sad noices come from {0}. It seems like he is in pain'.format(self.name))
                msgs.append('{0} is looking really down, he seems sick.'.format(self.name))
            if self.happy <= 60:
                new_title = '(︶︹︺)'
                msgs.append('No one is giving {0} attention. He seems like he wants to play'.format(self.name))
                msgs.append('{0} is looking sadly at his toys'.format(self.name))
                msgs.append('It seems like {0} is jumping around a lot. Maybe he wants to play'.format(self.name))
        
        elif lowest_value <= 80:
            if self.food <= 80:
                new_title = '(ﾉ･ｪ･)ﾉ'
                msgs.append('It seems like {0} is looking at the fridge. Maybe he is hungry'.format(self.name))
                msgs.append('One day {0} will figure out how to open the fridge...'.format(self.name))
                msgs.append('It looks like {0} said food, although you know he cannot talk...'.format(self.name))
            if self.health <= 80:
                new_title = '(-‿-)'
                msgs.append('It seems {0} doesnt have much energy lately'.format(self.name))
                msgs.append('{0} is coughing'.format(self.name))
                msgs.append('{0} seems not very active. Maybe he is getting sick'.format(self.name))
            if self.happy <= 80:
                new_title = '(-‿-)'
                msgs.append('{0} seems a bit bored. Someone should probably play with him'.format(self.name))
                msgs.append('{0} is watching tv, although he probably would like playing more'.format(self.name))
                msgs.append('Toys are made for playing - {0}'.format(self.name))
                msgs.append(''.format(self.name))
                msgs.append(''.format(self.name))
        else:
            username = random.choice(game.user_manager.users).name
            new_title = '(^‿^)'
            msgs.append('{0} keeps jumping around. He seems very happy'.format(self.name))
            msgs.append('{0} is taking a nap. He seems satisfied'.format(self.name))
            msgs.append('{0} loves {1} very much'.format(self.name,random.choice(game.user_manager.users).name))
            msgs.append('{0} looks very happy'.format(self.name))
            msgs.append('It seems that {0} is very comfortable'.format(self.name))
            msgs.append('{0} is doing an impression of {0}. It is quite good'.format(self.name,username))
            msgs.append('{0} likes {1}, and himself ofcourse.'.format(self.name,username))
        
        #%Add random
        if lowest_value >= 70 and True:
            msgs.append('Something breaks. {0} is looking guilty'.format(self.name))
            msgs.append('{0} has caught a bug! He seems very proud'.format(self.name))
            msgs.append('{0} decides he owns the fridge now'.format(self.name))
            msgs.append('{0} has caught a fly. He gives it as a present to {1}'.format(self.name,random.choice(game.user_manager.users).name))
            msgs.append('{0} is pretending to be an ananas'.format(self.name))
            
            
            
        game.controller.echo(random.choice(msgs))
        #Change title
        game.controller.change_title(new_title)
        
   #     controller.updater.bot.setChatTitle   
        
        
    def mood(self):
        status = self.get_status()
        lowest_status = min(self.get_status(), key = self.get_status().get)
        lowest_value = status[lowest_status]
        
        if lowest_value >= 80:
            msgs = ['{0} looks super happy, healthy and full',
                    '{0} looks like he is planning something, and he seems to be quite happy with it',
                    '{0} is looking very satisfied',
                    'happy noises are coming from {0}'
                    ]
        elif lowest_value >= 60:
            if self.health < 80 and self.food < 80:
                msgs = ['{0} looks a bit sickish and hungry']
            elif self.food < 80 and self.happy < 80:
                msgs = ['{0} wants attention and food']
            elif self.health < 80:
                msgs = ['{0} doesnt seem super healthy']
            elif self.food < 80:
                msgs = ['{0} is a bit hungry']
            else:
                msgs = ['{0} is looking a bit bored']
        elif lowest_value >= 30:
            if self.health < 60:
                msgs = ['{0} is feeling sick']
            elif self.food < 60:
                msgs = ['{0} is quite hungry']
            else:
                msgs = ['{0} is missing quite some attention']
        else:
            if self.health < 30:
                msgs = ['{0} seems very sick']
            elif self.food < 30:
                msgs = ['{0} is super hungry']
            else:
                msgs = ['{0} is very unhappy']
                
        
        game.controller.echo(random.choice(msgs).format(self.name))
                
    def pet_die(self,msg):
        self.alive = False
        game.controller.echo(msg)
        game.end_game()
            
        
    def is_bored(self,item_name):
        """
        Returns how bored the path is of a certain item
        0 : not bored at all
        1 : Starting to get bored (will accept, but no love bonus)
        2 : Does not accept
        """
        if item_name not in self.bored:
            self.bored[item_name] = 0
            
        if self.bored[item_name] <= 20:
            return 0
        elif self.bored[item_name] <= 40:
            return 1
        else:
            return 2
        
        
    def increase_bored(self,item_name,amount = 20):
        """
        Increase boredness of item
        """
        if item_name not in self.bored:
            self.bored[item_name] = 0
            
        self.bored[item_name] += amount
    
        
    

           
        

