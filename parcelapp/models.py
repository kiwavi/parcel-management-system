from django.db import models
from django.db.models.signals import post_save
from django.core.mail import send_mail
from decouple import config 
from datetime import date

# Create your models here.

date_today = date.today()


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
    parcel_number = models.CharField(max_length=64)
    status = models.CharField(max_length=16)
    status_alert = models.CharField(max_length=20)


def notify_sender_and_receiver(sender,instance,**kwargs):
    send_mail(
        'You Have Registered A Parcel',
        'This is to confirm that you have successfully registered parcel number ' + str(instance.parcel_number) + ' on ' + str(date_today),
        config('EMAIL_HOST_USER'),
        [instance.email_of_sender],
        fail_silently = False
    )

    send_mail(
        'You Will Receive A Parcel',
        'You will receive parcel number ' + str(instance.parcel_number) + ' .We will inform you once it reaches ' + instance.destination,
        config('EMAIL_HOST_USER'),
        [instance.email_of_receiver],
        fail_silently = False
    )

post_save.connect(notify_sender_and_receiver,sender=Parcel)
