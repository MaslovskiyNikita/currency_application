from django.core.management.base import BaseCommand
from src.apps.rates.models import Currency
from src.apps.integrations.nbrb.client import NBRBClient

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        client = NBRBClient()
        data = client.get_all_currencies()

        if not data:
            return []
        
        currencies_to_create = []
        existing_ids = set(Currency.objects.values_list('nbrb_id', flat=True))

        for item in data:
            if item['Cur_ID'] not in existing_ids:
                currencies_to_create.append(
                    Currency(
                        nbrb_id=item['Cur_ID'],
                        code=item['Cur_Code'],    
                        abbreviation=item['Cur_Abbreviation'],
                        name=item['Cur_Name']
                    )
                )

        Currency.objects.bulk_create(currencies_to_create)
        print(f"Added {len(currencies_to_create)} new currencies.")
