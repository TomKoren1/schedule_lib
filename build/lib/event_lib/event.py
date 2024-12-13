from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from .recurrence import Recurrence
from .reminder import Reminder
from .tag import Tag


@dataclass
class Event():
    title: str
    start_time: datetime
    end_time: datetime
    time_zone: str
    id: str

    location: Optional[str]=None
    description: Optional[str]=None
    base_event_id: Optional[str]=None
    recurrence: Optional[Recurrence]=None
    reminders: Optional[List[Reminder]]=None
    tag: Optional[List[Tag]]=None
    attendees: Optional[List[str]]=None
    google_calendar_id:Optional[str]=None
