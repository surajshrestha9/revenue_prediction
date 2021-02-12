from django.db import models

class Parameters(models.Model):
    year = models.IntegerField()
    total_arrival = models.IntegerField()
    average_length_of_stay = models.IntegerField()
    holiday_pleasure = models.IntegerField()
    pilgrimage = models.IntegerField()
    business = models.IntegerField()
    total_foreign_exchange = models.IntegerField()
    trekking_and_mountaineering = models.IntegerField()
    revenue = models.IntegerField()
    model = models.CharField(max_length=290)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.year)

