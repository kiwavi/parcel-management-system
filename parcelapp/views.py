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
import uuid

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
            self.entry.parcel_number = str(uuid.uuid4())
            self.entry.status = 'In transit'
            self.entry.status_alert = 'Not alerted'
            self.entry.save()
            self.form = form
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
        status_object = Parcel.objects.get(id=pk)
        if form.is_valid:
            status_object.status = 'Discharged'
            status_object.save()
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
            order.status_alert = 'Alerted'
            order.save() #you must save once you have altered a record from the view
        return self.form_valid(form)
        
    def form_valid(self,form):
        return super().form_valid(form)

