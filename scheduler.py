import threading

class Scheduler():
    """
    Schedules timed events
    """
    def __init__(self):
        self.stopped = False
        
    def create_timed_event(self,seconds,callback):
        def wrapped_callback():
            try:
                if not self.stopped:
                    callback()
            except KeyboardInterrupt:
                print('ctrl-c aborted timed event')
                
        event = threading.Timer(seconds,wrapped_callback)
        event.start()
        
    def stop(self):
        self.stopped = True