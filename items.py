from game import game

class Item():

        
    def use(self):
        'You cannot use this item'
        
    def remove(self):
        """
        Removes item from bag
        """
        game.user_manager.gcu().remove_item(self)
        
class Toy(Item):
    def __init__(self):
        self.score = 1
        
    def use(self):
        
        if game.pet.is_bored(self.name) == 0:
            game.controller.echo("%s loves playing with a %s" % (game.pet.name,self.name))
            game.pet.play(self.score,1)
            game.pet.increase_bored(self.name)
        elif game.pet.is_bored(self.name) == 1:
            game.controller.echo("%s plays with a %s. He doesnt seem very interested" % (game.pet.name,self.name))
            game.pet.play(self.score,0)
            game.pet.increase_bored(self.name)
        else:
            game.controller.echo("%s refuses to play with a %s" % (game.pet.name,self.name))

class Food(Item):
    def __init__(self):
        self.score = 1
        
    def use(self):
        bored = game.pet.is_bored(self.name)
        if bored == 0:
            game.controller.echo('{0} quickly eats his {1}. He seems to like it very much'.format(game.pet.name,self.name))
            game.pet.increase_bored(self.name)
            game.pet.feed(self.score,1)
            self.remove()
        elif bored == 1:
            game.controller.echo('{0} eats some {1}. He doesnt seem to be enjoying it'.format(game.pet.name,self.name))
            game.pet.increase_bored(self.name)
            game.pet.feed(self.score,0)
            self.remove()
        else:
            game.controller.echo('{0} looks with disgust to {1}. He is not eating that'.format(game.pet.name,self.name))
       
class Medicin(Item):
    def use(self):
        if game.pet.medicin_needed == self.name:
            game.pet.medicin_needed = None
            game.pet.health = 100
            self.remove()
        else:
            game.controller.echo('{0} does not need this'.format(game.pet.name))
    
    