class UserManager():
    
    def __init__(self):
        self.users = []
        self.current_user_id = 0
        
    def add_user(self,user):
        user.id = len(self.users)
        self.users.append(user)
        
    def gcu(self):
        """
        Get current user
        """
        return self.users[self.current_user_id]
        