from datetime import date, timedelta
from typing import Optional, List
from django.db import transaction
from src.apps.integrations.nbrb.client import NBRBClient
from src.apps.integrations.nbrb.dto import NBRBRateDTO
from src.apps.rates.models import Currency, Rate
import logging

logger = logging.getLogger(__name__)

class RateService:
    
    def load_with_history(self, target_date: date) -> bool:
        
        with NBRBClient() as client:
            current_loaded = self.load_rates_for_date(target_date, client=client)
            self.load_rates_for_date(target_date - timedelta(days=1), client=client)
        
        return current_loaded

    def load_rates_for_date(self, target_date: date, client: NBRBClient) -> bool:
        
        logger.info(f"Starting rate load for {target_date}")
        rates_dto = client.get_rates_on_date(target_date)
        
        if not rates_dto:
            logger.warning(f"No rates received for {target_date}")
            return False

        self._save_rates_to_db(rates_dto, target_date)
        
        return True

    @transaction.atomic
    def _save_rates_to_db(self, rates_dto: List[NBRBRateDTO], target_date: date):
        
        incoming_ids = [dto.cur_id for dto in rates_dto]
        currency_map = {
            c.nbrb_id: c 
            for c in Currency.objects.filter(nbrb_id__in=incoming_ids)
        }

        rates_to_create = []
        
        for dto in rates_dto:
            currency = currency_map.get(dto.cur_id)
            
            if currency:
                rates_to_create.append(
                    Rate(
                        currency=currency,
                        date=target_date,
                        scale=dto.scale,
                        official_rate=dto.official_rate
                    )
                )

        if rates_to_create:
            Rate.objects.bulk_create(
                rates_to_create,
                update_conflicts=True,
                unique_fields=['currency', 'date'],
                update_fields=['official_rate', 'scale']
            )
            logger.info(f"Successfully saved {len(rates_to_create)} rates for {target_date}")