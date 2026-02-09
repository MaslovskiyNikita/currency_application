import httpx
import logging
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from types import TracebackType

from src.apps.integrations.nbrb.dto import NBRBRateDTO

logger = logging.getLogger(__name__)

class NBRBClient:

    BASE_URL = "https://api.nbrb.by/exrates"

    def __init__(self) -> None:
        self._client = httpx.Client(
            base_url=self.BASE_URL,
            timeout=10.0,
            headers={
                "User-Agent": "NBRB-Integration-Service/1.0",
                "Accept": "application/json"
            }
        )

    def __enter__(self) -> "NBRBClient":
        return self

    def __exit__(
        self, 
        exc_type: Optional[type], 
        exc_val: Optional[Exception], 
        exc_tb: Optional[TracebackType]
    ) -> None:
        self.close()

    def close(self) -> None:
        try:
            self._client.close()
        except Exception as e:
            logger.warning(f"Error closing NBRB client: {e}")

    def get_all_currencies(self) -> list:
        try:
            response = self._client.get("currencies")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Failed to fetch currencies list: %s", e, exc_info=True)
            return []
        except Exception as e:
            logger.exception("Unexpected error fetching currencies: %s", e)
            return []

    def get_rates_on_date(self, target_date: date) -> List[NBRBRateDTO]:

        params = {
            "ondate": target_date.isoformat(),
            "periodicity": 0,
        }

        try:
            response = self._client.get("rates", params=params)

            if response.status_code == 404:
                logger.warning(f"NBRB returned 404 for date {target_date}")
                return []

            response.raise_for_status()
            data = response.json()
            
            if not data:
                logger.warning(f"NBRB returned empty list for {target_date}")
                return []

            logger.info("Successfully received %s rates for %s", len(data), target_date)
            return [self._map_to_dto(item) for item in data]

        except httpx.HTTPError as e:
            logger.error("NBRB API HTTP error: %s", e, exc_info=True)
            return []
        except Exception as e:
            logger.exception("Unexpected error fetching rates: %s", e)
            return []

    @staticmethod
    def _map_to_dto(data: dict) -> NBRBRateDTO:
        return NBRBRateDTO(
            cur_id=data["Cur_ID"],
            date=datetime.fromisoformat(data["Date"]),
            abbreviation=data["Cur_Abbreviation"],
            scale=data["Cur_Scale"],
            name=data["Cur_Name"],
            official_rate=Decimal(str(data["Cur_OfficialRate"])),
        )