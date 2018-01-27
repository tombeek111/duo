import json
class Settings():
    def __init__(self):
        self.settings = None
        
    def get_setting(self,path):
        """
        Gets setting from settings.json by array path
        """
        if not isinstance(path,list):
            path = [path]

        if self.settings == None:
            file = open('settings.json')
            self.settings = json.load(file)
            file.close()
        
        data = self.settings
        for name in path:
            data = data[name]
            
        return data