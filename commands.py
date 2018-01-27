from items import Toy,Food,Medicin
from game import game

class Command():
    
    def yesno(self,question,callback):
        """
        Ask yes or no question
        """
        
        #controller.echo(question + '\n1:yes \n0: no')
        def handle_response(ans):
            response = ans == 1
            callback(response)
            
            
        game.controller.request_choice(question,['no','yes'],handle_response)
            
        
    def request_points(self):
        pass
    
    def do(self):
        pass
    
    def call(self):
        pass

class Bag(Command):
    def __init__(self):
        pass
        
    def call(self):
        game.controller.echo('Money: {0}'.format(game.user_manager.gcu().money))
        choices = [item for item,qty in game.user_manager.gcu().item_qty.items() if qty > 0]
        
        def handle_choice(choice):
            item = game.user_manager.gcu().items[choices[choice]]
            item.use()
            
        game.controller.request_choice('Select an item:',choices,handle_choice)
        
class Pet(Command):
    def call(self):
        game.pet.pet()
    
class Shop(Command):

    def call(self):
        choices = ["{0} ${1}".format(item.name,item.price) for i,item in enumerate(self.items)]
        
        def handle_choice(choice):
            if choice is not None:
                item = self.items[choice]
                if game.user_manager.gcu().money < item.price:
                    game.controller.echo('You dont have enough money to buy a %s' % item.name)
                else:
                    game.user_manager.gcu().add_item(item)
                    game.user_manager.gcu().money -= item.price
                    game.controller.echo('You have bought a %s'%item.name)
                    
        game.controller.request_choice('What do you want to buy?',choices,handle_choice)

        
                
class Store(Shop):
    def __init__(self):
        self.items = []
        
        
        for key,item in game.settings.get_setting(['toys']).items():
            toy = Toy()
            toy.name = item['name']
            toy.price = item['price']
            toy.score = item['score']
            self.items.append(toy)
            
        for key,item in game.settings.get_setting(['foods']).items():
            food = Food()
            food.name = item['name']
            food.price = item['price']
            food.score = item['score']
            self.items.append(food)
        
class Pharmacy(Shop):
    def __init__(self):
        self.items = []
        
        for key,item in game.settings.get_setting(['medicin']).items():
            medicin = Medicin()
            medicin.name = item['name']
            medicin.price = item['price']         
            self.items.append(medicin)
      
        
                
class Vet(Command):
    def call(self):
        price = game.settings.get_setting(['prices','vet'])
        
        def handle_choice(answer):
            if answer:
                if game.user_manager.gcu().money >= price:
                    game.user_manager.gcu().money -= price
                    if game.pet.medicin_needed == None:
                        game.controller.echo('{0} seems completely fine. Thanks for the {1} euro'.format(game.pet.name,price))
                    else:
                        game.controller.echo('I recommend to give {0} some {1}'.format(game.pet.name,game.pet.medicin_needed))
                else:
                    game.controller.echo('You dont have enough money')
        self.yesno('Going to the vet costs {0}. Do you want to proceed'.format(price),handle_choice)
        
class WakeUp(Command):
    def call(self):
        game.pet.wake_up()
        