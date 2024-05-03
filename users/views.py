from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import authenticate, login
from .forms import CustomUserForm,EmailAuthenticationForm
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from registration.models import Registration
from booking.models import Booking
from vendor_profile.models import VendorProfile
from admin_profile.models import AdminProfile
from apis import serializers
from visits.models import Visits
from datetime import datetime, timedelta
import json

def create_data(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"home.html",{})  # Redirect to a success page after data is saved
    else:
        form = CustomUserForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    return render(request,"home.html",{})


def login_view(request):  
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=user_email, password=password)
            # print("email: ",user_email)
            # print("password: ",password)

            if user is not None:
                login(request, user)
                #return render(request,"super_home.html",{})  
                # return redirect('superuser/home')
                
                customUser= CustomUser.objects.get(email=user_email)
                if customUser.role=='super':
                    # return render(request,'super_home.html',{'token':token})
                    return redirect('superuser_home')
                elif customUser.role=='admin':
                    return redirect('admin_home')
                elif customUser.role=='vendor':
                    return redirect('vendor_home')
                else:
                    return render(request, 'login.html',{})
                    
            
        return render(request, 'login.html', {'login_failed': True}) 
        
    
            
    return render(request, 'login.html')


def logout_view(request):
  if request.method == 'POST':
    logout(request)
    return redirect('login') 
#   else:
#     return render(request, 'logout_confirmation.html', {})  # Optional: Confirmation page before logout


class SuperUserHome(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_vendors=VendorProfile.objects.all().count()
        total_admins=AdminProfile.objects.all().count()
        total_registration=Registration.objects.all().count()
        context={
            "total_registration":total_registration,
            "total_vendors":total_vendors,
            "total_admins":total_admins
        }   
        # if request.user.role == 'super':
        return render(request,'super_home.html',context=context)
        # return redirect('login')

class AdminHome(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # admin= AdminProfile.objects.get(id=request.user.admin_id)
        total_registration=Registration.objects.all().filter(admin__id=request.user.admin_id).count()
        total_vendors=VendorProfile.objects.all().filter(admin__id=request.user.admin_id).count()
        context={
            "total_registration":total_registration,
            "total_vendors":total_vendors,
            
        }   
        return render(request,'admin_home.html',context=context)

class VendorHome(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # if request.user.role == 'vendor':
        todays_visitors=Visits.objects.filter(
            stalls__vendor_id=request.user.vendor_id,
            created_at__gte=datetime.now().date(),
            created_at__lte=datetime.now().date() + timedelta(days=1)
        ).count()
        todays_bookings=Booking.objects.filter(
            stall__vendor_id=request.user.vendor_id,
            created_at__gte=datetime.now().date(),
            created_at__lte=datetime.now().date() + timedelta(days=1)
        ).count()
        visitors= Visits.objects.all().filter(stalls__vendor_id=request.user.vendor_id)
        bookings= Booking.objects.all().filter(stall__vendor_id=request.user.vendor_id)

        context={
            "todays_visitors":todays_visitors,
            "todays_bookings":todays_bookings,
            "total_visitors":visitors.count(),
            "total_bookings":bookings.count(),
            
        }
        return render(request,'vendor_home.html',context=context)
        # return redirect('login')

    def group_visitors_by_date(visitors):
        grouped_data = {}
        for visitor in visitors:
            date = visitor.created_at.date()  # Extract date from created_at
            if date not in grouped_data:
                grouped_data[date] = 0
            grouped_data[date] += 1
        return grouped_data
    
    def dashboard(request):
        visitors = Visits.objects.all()  # Fetch all visitors
        

    