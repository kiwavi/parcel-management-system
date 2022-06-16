from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ParcelForm
from .models import Parcel
import random
from datetime import date
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .forms import SearchParcelForm, DischargeForm, AcceptForm
from django.core.mail import send_mail
from django.views.generic.detail import SingleObjectMixin
from decouple import config 

date_today = date.today()

# Create your views here.

class HomePage(LoginRequiredMixin, FormView):
    ''' The hompegage: admin logs in and inputs order details  '''
    login_url = 'login'
    template_name = 'home.html'
    form_class = ParcelForm

    def form_valid(self,form):
        if form.is_valid:
            self.entry = form.save(commit=False)
            count = 0
            numbers = []
            while count < 4:
                number = random.randint(1,9)
                numbers.append(number)
                count = count + 1
            siku = str(date_today.year) + str(date_today.month) + str(date_today.day) + str(numbers[0]) + str(numbers[1]) + str(numbers[2]) + str(numbers[3])
            self.entry.parcel_number = siku
            self.entry.status = 'In transit'
            self.entry.status_alert = 'Not alerted'
            self.entry.save()
            self.form = form
            send_mail(
                'You Have Registered A Parcel',
                'This is to confirm that you have successfully registered parcel number ' + str(self.entry.parcel_number) + 'on ' + str(date_today),
                config('EMAIL_HOST_USER'),
                [self.entry.email_of_sender],
                fail_silently = False
            )

            send_mail(
                'You Will Receive A Parcel',
                'You will receive parcel number ' + str(self.entry.parcel_number) + ' .We will inform you once it reaches ' + self.entry.destination,
                config('EMAIL_HOST_USER'),
                [self.entry.email_of_receiver],
                fail_silently = False
            )
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self): # here, i'm passing the parcel number to the url success. the kwargs must also be included in urls.py
        return reverse('success', kwargs={'parcel':self.entry.parcel_number})


class Success(LoginRequiredMixin, TemplateView):
    ''' Redirected here after form  submission Homepage  '''
    login_url = 'login'
    template_name = 'success.html'

class ParcelArrival(LoginRequiredMixin, FormView):
    ''' Search for A Parcel Using Parcel Number  '''
    form_class = SearchParcelForm
    template_name = 'search.html'
    success_url = reverse_lazy('results')
    login_url = 'login'

class ParcelResults(LoginRequiredMixin, ListView):
    ''' User Redirected Here after Searching for A Parcel  '''
    template_name = 'results.html'
    model = Parcel
    
    def get_queryset(self):
        query = self.request.GET.get('parcel_number')
        if query:
            object_list = Parcel.objects.filter(parcel_number__contains=query)
            return object_list

class ParcelDetailView(LoginRequiredMixin, DetailView):
    ''' Detailed Description of Parcels  '''
    model = Parcel
    template_name = 'detailedresult.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        paper_status = self.object.status
        alert_status = self.object.status_alert
        context['parcel_status'] = paper_status
        context['alert_status'] = alert_status
        return context

class DischargeView(LoginRequiredMixin, FormMixin, DetailView):
    ''' Confirm with recipient that they have picked their parcel  '''
    template_name = 'discharge.html'
    form_class = DischargeForm
    login_url = 'login'
    model = Parcel

    def get_success_url(self):
        return reverse('detailedresult',kwargs={'pk':self.object.pk})

    def post(self,request,*args,**kwargs):
        form = self.get_form()
        self.object = self.get_object()
        pk = self.object.pk
        if form.is_valid:
            status_object = Parcel.objects.get(id=pk)
            status_object.status = 'Discharged'
            status_object.save()
            send_mail(
                'Confirmation that you picked',
                'This is to confirm that you have successfully received the parcel number ' + str(status_object.parcel_number) + 'on ' + str(date_today),
                config('EMAIL_HOST_USER'),
                [status_object.email_of_receiver],
                fail_silently = False
            )
            return self.form_valid(form)
            
    def form_valid(self,form):
        return super().form_valid(form)

class AlertView(LoginRequiredMixin, FormMixin, DetailView):
    ''' Alert Recipient That the Parcel has Arrived at The Destination  '''
    template_name = 'alert.html'
    form_class = AcceptForm
    model = Parcel
    login_url = 'login'

    def get_success_url(self):
        return reverse('detailedresult',kwargs={'pk':self.object.pk})
    
    def post(self,request,*args,**kwargs):
        form = self.get_form()
        self.object = self.get_object()
        pk = self.object.pk
        order = Parcel.objects.get(id=pk)
        if form.is_valid:
            send_mail(
                'Parcel has arrived',
                'Hello, this is to confirm that the parcel number ' + str(order.parcel_number) + ' sent to you from ' + order.from_location + ' on ' + str(order.date) + ' has arrived at ' + order.destination + '. Come pick the parcel at our ' + order.destination + ' offices.',
                config('EMAIL_HOST_USER'),
                [order.email_of_receiver],
                fail_silently = False
            )
            order.status_alert = 'Alerted'
            order.save() #you must save once you have altered a record from the view
        return self.form_valid(form)
        
        def form_valid(self,form):
            return super().form_valid(form)
