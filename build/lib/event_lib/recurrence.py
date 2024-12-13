from dataclasses import dataclass
from datetime import datetime
from typing import List,Optional

@dataclass
class Recurrence:
    id: str
    frequency: str
    interval: Optional[str]=None
    count: Optional[int]=None
    until: Optional[datetime]=None
    by: Optional[str]=None
    exception: Optional[List[datetime]]=None