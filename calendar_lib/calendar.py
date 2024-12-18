import datetime as dt
from event_lib.event import Event 
from dataclasses import dataclass
from typing import List,Optional

@dataclass
class Calendar():
    events:Optional[List[Event]]=None

    def __post_init__(self):
        if self.events is None:
            self.events = []
    
    # POST/create function
    def post_single_event(self,event:Event):
        self.events.append(event)
    def post_multiple_events(self,events:List[Event]):
        self.events.extend(events)

    # GET/read functions    
    def get_all_events(self)->List[Event]:
        return self.events
    def get_events_by_dates(self,start:dt,end:dt)->List[Event]:
        return [e for e in self.events if e.start_time>=start and e.end_time<=end]
    def get_event_by_id(self,id)->Event:
        for e in self.events:
            if e.id==id:
                return e
        return None

    # PUT/update functions
    def put_event(self,old_event:Event,new_event:Event):
        self.events[self.events.index(old_event)]=new_event
    def put_event(self,old_event_id:str,new_event:Event):
        index = next((i for i, event in enumerate(self.events) if event.id == old_event_id), None)
        if index is not None:
            self.events[index]=new_event
        else:
            raise ValueError(f'Event with id {old_event_id} not found.')

    # DELETE functions
    def delete_event_by_id(self,id):
        for e in self.events:
            if e.id == id:
                self.events.remove(e)
    def delete_event(self,event):
        self.events.remove(event)

