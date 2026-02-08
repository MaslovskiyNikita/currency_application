from datetime import date, timedelta
from django.db import transaction
from src.apps.integrations.nbrb.client import NBRBClient
from src.apps.rates.models import Currency, Rate
import logging

logger = logging.getLogger(__name__)

class RateService:
    def __init__(self):
        self.client = NBRBClient()

    @transaction.atomic
    def load_rates_for_date(self, target_date: date) -> bool:
        
        logger.info(f"Starting rate load for {target_date}")
        rates_dto = self.client.get_rates_on_date(target_date)
        if not rates_dto:
            logger.warning(f"No rates received for {target_date}")
            return False

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
            logger.info(f"Successfully saved {len(rates_to_create)} rates for {target_date}")
            Rate.objects.bulk_create(
                rates_to_create,
                update_conflicts=True,
                unique_fields=['currency', 'date'],
                update_fields=['official_rate', 'scale']
            )

    
    def load_with_history(self, target_date: date):

        self.load_rates_for_date(target_date)
        self.load_rates_for_date(target_date - timedelta(days=1))
        
        return True
        