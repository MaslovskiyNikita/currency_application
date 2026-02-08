from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

@dataclass()
class NBRBRateDTO:
    cur_id: int
    date: datetime
    abbreviation: str
    scale: int
    name: str
    official_rate: Decimal