from django.shortcuts import render,redirect
from .forms import StallForm
from datetime import datetime
import re
import os
from admin_profile.models import AdminProfile
from io import BytesIO
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Stalls
from categories.models import Categories
from vendor_profile.models import VendorProfile

# Create your views here.
def view_stall(request):
    
    vendor=VendorProfile.objects.get(id=request.user.vendor.id)
    categories= Categories.objects.all().filter(admin_id=vendor.admin.id)
    stalls = Stalls.objects.get(vendor=request.user.vendor.id)
    admin= AdminProfile.objects.get(id=vendor.admin.id)
    
    
    
    return render(request,'add_stall.html',{"categories":categories,"stall":stalls,"vendor":vendor,"admin":admin})

def create_stall(request):
    if request.method=='POST':
        form= StallForm(request.POST)
        log_url=""
        catalog_url=""
        banner_url=""
        if form.is_valid():
            stall= Stalls.objects.get(vendor=request.user.vendor.id)
            print("update")
            logo= request.FILES.get('logo')
            if logo:
                if stall.logo:
                    filename= stall.logo
                    os.remove(os.path.join(settings.MEDIA_ROOT, filename))
                else:
                    filename= str(datetime.now())+'_'+(logo.name)
                    filename = re.sub(r'[^\w\-.]', '_', filename)
                fs = FileSystemStorage(location=settings.MEDIA_ROOT )
                filename = fs.save(filename, logo)
                log_url = filename
            else:
                log_url= stall.logo
            
            catalog= request.FILES.get('catalog')
            if catalog:
                if stall.catalog:
                    filename= stall.catalog
                    os.remove(os.path.join(settings.MEDIA_ROOT, filename))
                else:
                    filename= str(datetime.now())+'_'+(catalog.name)
                    filename = re.sub(r'[^\w\-.]', '_', filename)
                fs = FileSystemStorage(location=settings.MEDIA_ROOT )
                filename = fs.save(filename, catalog)
                catalog_url = filename
            else:
                catalog_url= stall.catalog

            banner= request.FILES.get('banner')
            if banner:
                if stall.banner:
                    filename= stall.banner
                    os.remove(os.path.join(settings.MEDIA_ROOT, filename))
                    print(" stall upadate file removed suc")
                else:
                    filename= str(datetime.now())+'_'+(banner.name)
                    filename = re.sub(r'[^\w\-.]', '_', filename)
                fs = FileSystemStorage(location=settings.MEDIA_ROOT )
                filename = fs.save(filename, banner)
                banner_url = filename
            else:
                banner_url= stall.banner

            category=  Categories.objects.get(id=form.cleaned_data['cate_type'])

            stall.stall_name= request.POST.get('shop_name')
            stall.logo= log_url
            stall.about= form.cleaned_data['about_stall']
            stall.email= form.cleaned_data['email']
            stall.contact= form.cleaned_data['contact']
            stall.category= category
            stall.vendor_id= request.user.vendor.id
            stall.city= form.cleaned_data['city']
            # stall.cat_type= form.cleaned_data['type']
            stall.catalog= catalog_url
            stall.banner= banner_url
            stall.address= form.cleaned_data['address']
            
            stall.save()
            
            return redirect("add_stall")
        else:
            return render(request,'add_stall.html',{"form":form})
    return redirect("add_stall")