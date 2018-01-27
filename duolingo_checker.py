from game import game

class DuolingoChecker:
    def __init__(self,users):
        self.users = users
        
    def get_added_xp(self):
        """
        Gets for each user amount of new duolingo xp.
        Returns None for a user if there was an error
        """
        added_xp = {}
        for user in self.users:
            initial_xp = user.duolingo_xp
            new_xp = user.get_duolingo_xp()
            if new_xp is not None:
                added_xp[user.id] = new_xp-initial_xp
        return added_xp
    
    
    def schedule(self,time):
        def check():
            xp = self.get_added_xp()
            #Check if requests were succesfull
            success = True
            for user,user_xp in xp.items():
                if user_xp is None:
                    success = False
            if success:
                for user_id,user_xp in xp.items():
                    if user_xp > 0:
                        user = game.user_manager.users[user_id]
                        money = round(game.settings.get_setting(['money_per_duolingo_xp'])*user_xp)
                        user.money += money
                        user.duolingo_xp += user_xp
                        game.controller.echo('{0} earned ${1} by playing duolingo. Well done!'.format(user.name,money))
                self.schedule(60)
            else:
                self.schedule(10)
                print('error in getting xp')
        game.scheduler.create_timed_event(time,check)