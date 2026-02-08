from django.db import models

class Currency(models.Model):
    nbrb_id = models.IntegerField(unique=True)
    code = models.CharField(max_length=3)
    abbreviation = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Currency_data"

    def __str__(self):
        return f"{self.abbreviation} ({self.name})"


class Rate(models.Model):
    currency = models.ForeignKey(
        Currency, 
        on_delete=models.CASCADE, 
        related_name="rates",
    )
    date = models.DateField()
    scale = models.IntegerField()
    official_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=4, 
    )

    class Meta:
        unique_together = ('currency', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.currency.abbreviation} on {self.date}: {self.official_rate}"