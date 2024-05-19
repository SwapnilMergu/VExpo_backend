from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import VendorForm
from .models import VendorProfile
from .forms import VendorProfileForm
from stalls.models import Stalls
from users.models import CustomUser
from django.core.mail import send_mail
from visits.models import Visits
from django.db import connection
from visitors.models import Visitors
from booking.models import Booking
from django.conf import settings
from categories.models import Categories
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
import pandas as pd
import json
import random
import string
import re 
import os
from datetime import datetime, date
from django.utils import timezone

# Create your views here.
def view_vendor(request):
    vendor_list = VendorProfile.objects.all().filter(admin=request.user.admin.id)
    # print(AdminRegister.objects.all())
    return render(request, 'view_vendors.html', {'user_list': vendor_list})

def create_vendor(request):
    categories= Categories.objects.all().filter(admin_id=request.user.admin.id)
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            # print(form)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            contact = form.cleaned_data['contact']
            category_id = request.POST['category']

            category = Categories.objects.get(id=category_id)
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            en_password= make_password(password)
            
            
            vendor= VendorProfile.objects.create(
                full_name=name,
                email=email,
                contact= contact,
                password=en_password,
                admin= request.user.admin,
                rating=0
            )
            
            user= CustomUser.objects.create(
                email=email,
                password= en_password,
                vendor= vendor,
                role= "vendor"
            )
            stall=Stalls.objects.create(
                vendor=vendor,
                email=email,
                contact= contact,
                category= category,
                rating=0,
                visits=0
            )

            send_mail(
                'V Expo',
                f'Hi {name}, Welcome to V Expo. Your password is: {password}',
                settings.EMAIL_HOST_USER,
                ['swapnil.mergu05@gmail.com'],
                fail_silently=False,)
            
            return redirect('view_vendor')
        else:
            return render(request, 'add_vendor.html', {'form': form})
        
    return render(request,'add_vendor.html',{"categories":categories})

def update_vendor(request, pk):
    categories= Categories.objects.all().filter(admin_id=request.user.admin.id)
    vendor = get_object_or_404(VendorProfile,pk=pk)
    stall= Stalls.objects.get(vendor=vendor)
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            category_id=request.POST.get('category')
            category = Categories.objects.get(id=category_id)
            vendor.full_name = request.POST.get('name')
            vendor.email = request.POST.get('email')
            vendor.contact = request.POST.get('contact')
            vendor.save()
            
            customUser= CustomUser.objects.get(vendor_id=pk)
            customUser.email = request.POST.get('email')
            customUser.save()  


            stall.email= request.POST.get('email')
            stall.contact= request.POST.get('contact')
            stall.category = category
            stall.save()

            return redirect('view_vendor')  

        else:
            return render(request, 'update_vendor.html', {'vendor':vendor,'form': form})
        
        # admin.save()
        #return redirect('item_list')
    # print("\n\ncontact:  ",vendor.contact)
    return render(request, 'update_vendor.html', {'vendor': vendor,"stall":stall,"categories":categories})


def delete_vendor(request, pk):
    vendor_profile = get_object_or_404(VendorProfile, pk=pk)
    if request.method == 'POST':
        user= CustomUser.objects.get(vendor_id=pk)
        vendor_profile.delete()
        user.delete()   
        return redirect('view_vendor')
    return render(request,'view_vendor.html',{'deletion':'<script>alert("Deletection failed")</script>'})


def users_visited(request):
    stall= Stalls.objects.get(vendor_id=request.user.vendor.id)
    # visits= Visits.objects.all().filter(stalls=stall.id)
    today= date.today()
    # input_date= "18/05/2024"
    # day, month, year = map(int, input_date.split('/'))
    # date_obj = date(year,month,day)
    # date_obj= date_obj.format("%d/%m/%Y")
    # print("\n\n date_obj : ",date_obj,"\n\n")
    visitors= Visits.objects.select_related('visitors', 'stalls').filter(stalls=stall.id).filter(created_at__startswith=today)
    # with connection.cursor() as cursor:
    #     query="""
    #         SELECT v.first_name, v.last_name, v.contact, vs.rating, vs.review ,vs.created_at
    #         FROM visits AS vs
    #         INNER JOIN visitors AS v 
    #         ON v.id = vs.visitor_id
    #         WHERE vs.stall_id = %s
    #     """
    #     cursor.execute(query,[stall.id])
    #     rows = cursor.fetchall()
    #     print("Data : ",rows)
    # data= Visitors.objects.raw('SELECT v.first_name, v.last_name, v.contact, vs.rating, vs.created_at  FROM visitors as v INNER JOIN visits as vs ON vs.visitor_id=v.id')
    
    # rows = data.fetchall()

    return render(request,"users_visited.html",{"visitors":visitors})



def users_bookings(request):
    vendor= VendorProfile.objects.get(id=request.user.vendor.id)
    stall= Stalls.objects.get(vendor=vendor)
    today= date.today()
    today= today.strftime("%d/%m/%Y")
    booking= Booking.objects.all().filter(stall=stall).filter(date=today)
    # visitors= Visits.objects.select_related('visitors', 'stalls').filter(stalls=stall.id)
    return render(request,"users_bookings.html",{"bookings":booking})

def reject_booking(request, pk):
    booking= Booking.objects.get(id=pk)
    booking.status= "rejected"
    booking.save()
    return redirect('users_bookings')

def accept_booking(request, pk):
    booking= Booking.objects.get(id=pk)
    booking.status= "accepted"
    booking.save()
    return redirect('users_bookings')

#vendor edit

def view_profile(request):
    vendor= VendorProfile.objects.get(id=request.user.vendor.id)
    

    if vendor.social_links=="":
        social_links=None
    else:
        social_links= json.loads(vendor.social_links)

    return render(request,"update_profile.html",{"vendor":vendor,"social_links":social_links})

def vendor_edit(request):
    pass

def edit_profile(request):
    print("update")
    if request.method == 'POST':
        vendor= VendorProfile.objects.get(id=request.user.vendor.id)
        if vendor.social_links=="":
            social_links=None
        else:
            social_links= json.loads(vendor.social_links)
        form= VendorProfileForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            contact = request.POST.get('contact')
            whatsapp_no = request.POST.get('whatsapp_no')
            dob = request.POST.get('dob')
            address = request.POST.get('address')
            city = request.POST.get('city')
            facebook = request.POST.get('facebook')
            instagram = request.POST.get('instagram')
            twitter = request.POST.get('twitter')
            linked_in = request.POST.get('linked_in')
            youtube = request.POST.get('youtube')
            
            # Update the User model
            user = CustomUser.objects.get(vendor=request.user.vendor)
            user.email = email
            user.save()

            # Update the VendorProfile model
            vendor.full_name = name
            vendor.contact = contact
            vendor.email = email
            vendor.address = address
            vendor.city = city
            vendor.DOB = dob
            vendor.whatsapp_no = whatsapp_no

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
                
            social_links['whatsapp_no'] = whatsapp_no

            vendor.social_links = json.dumps(social_links)
            vendor.status = 1
            # vendor.save()
            
            # Handle file upload if any
            file = request.FILES.get('profile')
            if file:
                # filename = f'file/{id}_{file.name}'
                filename= str(datetime.now())+'_'+(file.name)
                filename = re.sub(r'[^\w\-.]', '_', filename)
                fs = FileSystemStorage(location=settings.MEDIA_ROOT )
                filename = fs.save(filename, file)
                uploaded_file_url = fs.url(filename)
                vendor.profile = filename
            vendor.save()

            return redirect('view_profile')  # Adjust the redirect URL as needed
        
        else:
            return render(request, 'update_profile.html', {"form":form,"vendor":vendor,"social_links":social_links})
    return render(request,"update_profile.html",{})


def export_vendor_to_excel(request):
    # Fetch data from your model
    data = VendorProfile.objects.all().filter(admin_id=request.user.admin.id).values("full_name", "email", "contact", "address")

    # Convert queryset to DataFrame
    df = pd.DataFrame(list(data))

    # Create a HttpResponse object with the appropriate Excel headers
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename='+str(datetime.now().date())+'_data.xlsx'

    # Use Pandas to create an Excel writer and save the DataFrame to it
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response


def export_users_visited_to_excel(request):
    # Fetch data from your model
    data = Visits.objects.all().filter(stalls__vendor_id=request.user.vendor.id).values("visitors__first_name", "visitors__last_name", "visitors__email", "visitors__contact","rating","review","created_at")

    # Convert queryset to DataFrame
    df = pd.DataFrame(list(data))

    for col in ['created_at']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: timezone.localtime(x).replace(tzinfo=None) if pd.notnull(x) else x)
    

    # Create a HttpResponse object with the appropriate Excel headers
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename='+str(datetime.now().date())+'_data.xlsx'

    # Use Pandas to create an Excel writer and save the DataFrame to it
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response

def export_users_bookings_to_excel(request):
    # Fetch data from your model
    vendor= VendorProfile.objects.get(id=request.user.vendor.id)
    stall= Stalls.objects.get(vendor=vendor)
    data= Booking.objects.all().filter(stall=stall).values("visitor__first_name", "visitor__last_name", "visitor__email","visitor__contact","interest","time","date","status")

    # Convert queryset to DataFrame
    df = pd.DataFrame(list(data))
   
    # Create a HttpResponse object with the appropriate Excel headers
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename='+str(datetime.now().date())+'_data.xlsx'

    # Use Pandas to create an Excel writer and save the DataFrame to it
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response