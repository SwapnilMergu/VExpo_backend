from django.shortcuts import render, redirect, get_object_or_404
from admin_profile.models import AdminProfile
from admin_profile.forms import AdminForm
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from categories.models import Categories
from .forms import AdminProfileForm
from users.models import CustomUser
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.files.storage import FileSystemStorage
import pandas as pd
import json
import random
import string
import os
import re
import json
from datetime import datetime


def admin_list(request):
    admin_list = AdminProfile.objects.all()
    # print(AdminRegister.objects.all())
    return render(request, 'view_admin.html', {'user_list': admin_list})

def create_admin(request):

    categories= Categories.objects.all().filter(superuser_id=request.user.id)
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            contact = form.cleaned_data['contact']
            category_id = form.cleaned_data['category']
            category = Categories.objects.get(id=category_id)
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            en_password= make_password(password)
            admin_data= AdminProfile.objects.create(
                full_name=name,
                email=email,
                contact= contact,
                category= category,
                password= en_password
            )
            CustomUser.objects.create(
                email=email,
                password= en_password,
                admin= admin_data,
                role= "admin"
            )

            send_mail(
                'Welcome to Vertex Technosys',
                f'Hi {name},\nWelcome to V Expo.\nYour password is: {password}',
                settings.EMAIL_HOST_USER,
                ['swapnil.mergu05@gmail.com'],#[email],
                fail_silently=False,)
            
            return redirect('view_admin')
        else:
            return render(request, 'add_admin.html', {'form': form})
        
    return render(request,'add_admin.html',{"categories":categories})

def update_admin(request, pk):
    admin = get_object_or_404(AdminProfile,pk=pk)
    categories= Categories.objects.all().filter(superuser_id=request.user.id)
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            admin.full_name = request.POST.get('name')
            admin.contact = request.POST.get('contact')
            admin.category = Categories.objects.get(id=request.POST.get('category'))

            admin.save()

            customUser= CustomUser.objects.get(admin=pk)
            customUser.email = request.POST.get('email')
            customUser.save()            

            #print(customUser.email)

            return redirect('view_admin')  

        else:
            return render(request, 'update_admin.html', {'admin':admin,'form': form})
        
        # admin.save()
        #return redirect('item_list')
    return render(request, 'update_admin.html', {'admin': admin,"categories":categories})


def delete_admin(request, pk):
    admin = get_object_or_404(AdminProfile, pk=pk)
    if request.method == 'POST':
        user= CustomUser.objects.filter(admin=pk)
        admin.delete()
        user.delete()
        return redirect('view_admin')
    return render(request,'view_admin.html',{'deletion':'<script>alert("Deletection failed")</script>'})


#organizer admin profile
def organizer_profile(request):
    categories= Categories.objects.filter(admin_id=None)
    print(request.user.admin)
    admin = AdminProfile.objects.get(id=request.user.admin.id)
    if admin.social_links=="":
        social_links=None
    else:
        social_links= json.loads(admin.social_links)
    
    
    return render(request,"update_admin_profile.html",{"categories":categories,"admin":admin,"social_links":social_links})


def update_admin_profile(request):
    if request.method=='POST':
        print(request.POST)
        categories= Categories.objects.filter(admin_id=None)
        admin = AdminProfile.objects.get(id=request.user.admin.id)
        if admin.social_links=="":
            social_links=None
        else:
            social_links= json.loads(admin.social_links)
        
        
        form= AdminProfileForm(request.POST)
        log_url=""
        catalog_url=""
        banner_url=""
        if form.is_valid():
            # if admin.catalog:
            #     data={}
            #     data['role']='admin'
            #     data['admin_id']=request.user.admin.id
            #     print(data)
                
            logo= request.FILES.get('logo')
            print("\n\n Inside if valid \n\n")

            if logo:
                if admin.logo:
                    print("\n\n Inside if logo exisits: ",admin.logo," \n\n")
                    filename= admin.logo
                    os.remove(os.path.join(settings.MEDIA_ROOT, filename))
                else:
                    filename= str(datetime.now())+'_'+(logo.name)
                    filename = re.sub(r'[^\w\-.]', '_', filename)
                
                fs = FileSystemStorage(location=settings.MEDIA_ROOT )
                filename = fs.save(filename, logo)
                log_url = filename
                print("\n\n filename after add: ",filename," \n\n")
            else:
                log_url= admin.logo
            
            catalog= request.FILES.get('catalog')
            if catalog:
                if admin.catalog:
                    filename= admin.catalog
                    os.remove(os.path.join(settings.MEDIA_ROOT, filename))
                else:
                    filename= str(datetime.now())+'_'+(catalog.name)
                    filename = re.sub(r'[^\w\-.]', '_', filename)
                fs = FileSystemStorage(location=settings.MEDIA_ROOT )
                filename = fs.save(filename, catalog)
                catalog_url = filename
            else:
                catalog_url= admin.catalog

            banner= request.FILES.get('banner')
            if banner:
                if admin.banner:
                    filename= admin.banner
                    os.remove(os.path.join(settings.MEDIA_ROOT, filename))
                else:
                    filename= str(datetime.now())+'_'+(banner.name)
                    filename = re.sub(r'[^\w\-.]', '_', filename)
                fs = FileSystemStorage(location=settings.MEDIA_ROOT )
                filename = fs.save(filename, banner)
                banner_url = filename
            else:
                banner_url= admin.banner

            category=''
            if request.POST.get('category'):
                category= Categories.objects.get(id=int(request.POST.get('category')))
            
            admin.full_name= form.cleaned_data['full_name']
            admin.event_name= form.cleaned_data['event_name']
            admin.contact= form.cleaned_data['contact']
            # admin.email= form.cleaned_data['email']
            admin.password= request.user.password
            admin.address= form.cleaned_data['address']
            admin.DOB= request.POST.get('dob')
            admin.start_date= request.POST.get('start_date')
            admin.end_date= request.POST.get('end_date')
            admin.price= request.POST.get('price')
            admin.whatsapp_no= form.cleaned_data['whatsapp_no']
            admin.about= request.POST.get('about_event')
            admin.category= category
            admin.logo= log_url
            admin.catalog= catalog_url
            admin.banner= banner_url
            admin.city = request.POST.get('city')
            facebook = request.POST.get('facebook')
            instagram = request.POST.get('instagram')
            twitter = request.POST.get('twitter')
            linked_in = request.POST.get('linked_in')
            youtube = request.POST.get('youtube')
            # print("category : ",admin.category.id," : ",type(admin.category))
            # Update the social links
            social_links = {}
            if facebook:
                social_links['facebook'] = facebook
            if instagram:
                social_links['instagram'] = instagram
            if twitter:
                social_links['twitter'] = twitter
            if linked_in:
                social_links['linked_in'] = linked_in
            if youtube:
                social_links['youtube'] = youtube
            
            social_links['whatsapp_no'] = form.cleaned_data['whatsapp_no']

            print(admin.category)

            admin.social_links = json.dumps(social_links)
            admin.status = 1
            admin.save()


            print("\n\n Done \n\n")

            return redirect("organizer_profile")
        
        else:
            print("\n\n Inside if invalid ",form.errors,"\n\n")
            return render(request,"update_admin_profile.html",{"categories":categories,"admin":admin,"social_links":social_links,"form":form})
    return redirect("organizer_profile")


def export_admin_to_excel(request):
    # Fetch data from your model
    data = AdminProfile.objects.all().values("full_name", "email", "contact", "city","address","start_date","end_date","price","category__cname")

    # Convert queryset to DataFrame
    df = pd.DataFrame(list(data))

    # Create a HttpResponse object with the appropriate Excel headers
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename='+str(datetime.now().date())+'_data.xlsx'

    # Use Pandas to create an Excel writer and save the DataFrame to it
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response