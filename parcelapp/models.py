from django.db import models

# Create your models here.

CATEGORY_CHOICES = [
    ('Small Electronic','Small Electronic'),
    ('Envelope','Envelope'),
    ('Big electronic', 'Big electronic'),
    ('Food', 'Food'),
]

class Parcel(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=17)
    from_location = models.CharField(max_length=20)
    destination = models.CharField(max_length=18)
    id_number_sender = models.PositiveIntegerField()
    id_number_receiver =  models.PositiveIntegerField()
    email_of_sender = models.EmailField()
    email_of_receiver = models.EmailField()
    date = models.DateField(auto_now=True)
    parcel_number = models.PositiveIntegerField(unique=True)
    status = models.CharField(max_length=16)
    status_alert = models.CharField(max_length=20)


    
