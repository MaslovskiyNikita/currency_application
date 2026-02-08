import httpx
import logging
from datetime import date
from typing import List
from decimal import Decimal
from datetime import datetime
from src.apps.integrations.nbrb.dto import NBRBRateDTO
logger = logging.getLogger(__name__)

class NBRBClient:
    BASE_URL = "https://api.nbrb.by/exrates"


    def get_all_currencies(self):
        
        try:
            
            with httpx.Client(timeout=10.0, verify=False) as client:
                response = client.get(f"{self.BASE_URL}/currencies")
                response.raise_for_status()
                return response.json() 
        except Exception as e:
            return []

    def get_rates_on_date(self, target_date: date) -> List[NBRBRateDTO]:
        params = {
            "ondate": target_date.isoformat(),
            "periodicity": 0
        }
        
        with httpx.Client(timeout=10.0, verify=False) as client:
            try:
                response = client.get(f"{self.BASE_URL}/rates", params=params)
                
                if response.status_code == 404:
                    return []
                
                response.raise_for_status()
                data = response.json()
                logger.info(f"Received {len(data)} rates from NBRB")
                return [self._map_to_dto(item) for item in data]
                
            except (httpx.HTTPError, Exception) as e:
                logger.error(f"NBRB API error: {e}", exc_info=True)
                return []

    def _map_to_dto(self, data: dict) -> NBRBRateDTO:
        return NBRBRateDTO(
            cur_id=data["Cur_ID"],
            date=datetime.fromisoformat(data["Date"]),
            abbreviation=data["Cur_Abbreviation"],
            scale=data["Cur_Scale"],
            name=data["Cur_Name"],
            official_rate=Decimal(str(data["Cur_OfficialRate"]))
        )