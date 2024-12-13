from dataclasses import dataclass

@dataclass
class Reminder:
    defult_minutes=30
    defult_method=2
    
    id: str
    """ 1: email, 2: popup """
    method: int 
    minutes: int

    def defult(self):
        return Reminder(self.defult_method,self.defult_minutes)
    
    def change_defult(self,method,minutes):
        self.defult_method=method
        self.defult_minutes=minutes