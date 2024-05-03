from django.shortcuts import render,HttpResponse,get_object_or_404
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import CustomUser
from admin_profile.models import AdminProfile
from django.contrib.auth.hashers import make_password
from visitors.models import Visitors
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from .customAuth import CustomAuthentication, CustomExceptionHandler
from vendor_profile.models import VendorProfile
from visits.models import Visits
from django.core.serializers import serialize
from stalls.models import Stalls
import calendar
from booking.models import Booking
from wishlist.models import Wishlist
from registration.models import Registration
from datetime import datetime, timedelta
from collections import defaultdict
from django.db.models import Q
from datetime import date
import os
import random
import string
import json
from . import serializers

#visitors view

# class PasswordDemo(APIView):
#     authentication_classes = []
#     permission_classes = []
#     def get(self, request):
#         pas= make_password("vendor@123")
#         return JsonResponse({"status":"sucess","msg":""+pas})

class VisitorsRegistrationView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, format=None):
        # email= request.data['email']
        # password= request.data['password']
        # contact= request.data['contact']
        # first_name= request.data['first_name']
        # last_name= request.data['last_name']
        # user = Visitors.objects.create(
        #     first_name=first_name,
        #     last_name=last_name,
        #     email=email,
        #     contact=contact,
        #     password=make_password(password),
        # )
        chars= string.ascii_letters + string.digits + '!@#$%^&*()_'
        random.seed(os.urandom(1024))
        password= ''.join(random.choice(chars) for i in range(13))
        serializer = serializers.VisitorsSerializer(data=request.data)
        if serializer.is_valid():
            Visitors.objects.create(
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                email=request.data['email'],
                contact=request.data['contact'],
                password=make_password(password),
            )
            visitor= Visitors.objects.get(contact=request.data['contact'])
            
            serializerVisitor= serializers.VisitorsSerializer(visitor)
            token= RefreshToken.for_user(visitor) 
            return Response({"status":"success",'msg': 'User created successfully',"token":str(token.access_token), "visitor":serializerVisitor.data},status=200)  
        return Response({"status":"failed",'msg': 'User failed successfully',"error":serializer.errors},status=400)

# Visitor login view
class VisitorsLoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, format=None):
        contact= request.data['contact']
        visitor=None
        try:
            visitor= Visitors.objects.get(contact=contact)
        except:
            return Response({"status":"faild","msg":"User not registered"},status=400)
        if visitor:
                serializer= serializers.VisitorsSerializer(visitor)
                refresh = RefreshToken.for_user(visitor)  # Generate tokens using the visitor object
                return Response({"status":"sucess",
                                    "token":str(refresh.access_token),
                                    "visitor":serializer.data},
                                    status=200)
        return Response({'msg': 'User failed successfully',"error":"invalid credentials"},status=400)
     

class VisitorsView(CustomExceptionHandler,APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        visitors = Visitors.objects.all()
        serializer = serializers.VisitorsSerializer(visitors, many=True)
        return Response({"status":"success",'data': serializer.data},status=200)
    
    def get(self, request, pk, format=None):
        visitors = Visitors.objects.get(id=pk)
        serializer = serializers.VisitorsSerializer(visitors)
        return Response({"status":"success",'data': serializer.data},status=200)
    
    def put(self, request, pk, format=None):
        visitor = get_object_or_404(Visitors, pk=pk)
        if visitor:
            serializer = serializers.VisitorsSerializer(visitor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status":"success",'msg': 'visitor data updated successfully'},status=200)  
        return Response({"status":"failed",'msg': 'failed to update user',"error":serializer.errors},status=400)

    def delete(self, request, pk, format=None):
        visitor = get_object_or_404(Visitors, pk=pk)
        if visitor:
            visitor.delete()
            return Response({"status":"success",'msg': 'visitor data deleted successfully'},status=200)  
        return Response({"status":"failed",'msg': 'failed to delete user'},status=400)
    
#get Stall
class StallView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id, format=None):
        stalls = Stalls.objects.get(id=id)
        serializer = serializers.StallsSerializer(stalls)
        return Response({"status":"success",'stall': serializer.data},status=200)

#Visitor stall visit
class VisitorStallVisitView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        stall= get_object_or_404(Stalls, id=request.data["stall_id"])
        if stall.vendor:

            if request.data["stall_id"] and request.data["visitor_id"] and request.data["rating"]:
                visit= Visits.objects.create(
                    visitors=Visitors.objects.get(id=request.data["visitor_id"]),
                    stalls=Stalls.objects.get(id=request.data["stall_id"]),
                    rating=int(request.data["rating"]),
                    review=request.data["review"]
                )
                print("\n\nvisit rating type : ",type(visit.rating),"\n\n")
                if visit.rating>1:
                    if stall.rating<1:
                        stall.rating=visit.rating
                    else:
                        print("\n\nstall rating :",(stall.rating+visit.rating)/2)
                        stall.rating= (stall.rating+visit.rating)/2
                stall.stall_visits=stall.stall_visits+1
                stall.save()

                serializer = serializers.StallsSerializer(stall)

                return Response({"status":"success",'msg': 'visitor data updated successfully',"stall":serializer.data},status=200)
            else:
                return Response({"status":"failed 1",'msg': 'failed to update user',"error":"Some fileds are missing"},status=200)
                
        return Response({"status":"failed",'msg': 'failed to update user'},status=200)
        # return Response({"status":"failed",'msg': 'failed to update user',"error":serializer.errors},status=400)

#Exhibition Registration
class ExhibitionRegistrationView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, visitor_id, format=None):
        registration=None
        try:
            registration= Registration.objects.all().filter(visitor=visitor_id)
            print("registration : ",registration)
        except:
            return JsonResponse({"status":"faild","msg":"User not registered"},status=400)
        if registration:
                print("registration true ")
                serializer= serializers.RegistrationSerializer(registration, many=True)
                
                return Response({"status":"sucess",
                                    "registrations":serializer.data},
                                    status=200)
        return JsonResponse({'msg': 'User failed successfully',"error":"invalid credentials"},status=400)
    
    def post(self, request, format=None):
        print(request.data)
        # serializer = serializers.RegistrationSerializer(data=request.data)
        if request.data.get('visitor_id') and request.data.get('admin_id'):
            admin= get_object_or_404(AdminProfile, pk=request.data.get('admin_id'))
            visitor= get_object_or_404(Visitors, pk=request.data.get('visitor_id'))
            registration= Registration(admin=admin,visitor=visitor)
            registration.save()
            return Response({"status":"success",'msg': 'registration successfully'},status=200) 
        return Response({"status":"failed",'msg': 'failed to update user'},status=400)

#Wishlist
class WishlistView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, visitor_id, format=None):
        wishlist= Wishlist.objects.all().filter(visitor=visitor_id)
        print("wishlist : ",wishlist)
        serializer= serializers.WishlsitSerializer(wishlist, many=True)
        
        return Response({"status":"sucess",
                            "wishlist":serializer.data},
                            status=200)
    
    def post(self, request, format=None):
        print(request.data)
        # serializer = serializers.RegistrationSerializer(data=request.data)
        if request.data.get('visitor_id') and request.data.get('admin_id'):
            admin= get_object_or_404(AdminProfile, pk=request.data.get('admin_id'))
            visitor= get_object_or_404(Visitors, pk=request.data.get('visitor_id'))
            wishlist= Wishlist(admin=admin,visitor=visitor)
            wishlist.save()
            return Response({"status":"success",'msg': 'wishlist successfully'},status=200) 
        return Response({"status":"failed",'msg': 'failed to update user'},status=400)
    
#Booking
class BookingView(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, visitor_id, format=None):
        booking = Booking.objects.all().filter(visitor=visitor_id)
        
        # vendor_registers = VendorRegister.objects.all()
        # data = []
        # for b in booking:
        #     vendor_profile = VendorProfile.objects.get(id=)
            
        #     serializer = serializers.BookingAPISerializer(
        #         {'vendor_profile': vendor_profile, 'booking': b}
        #     )
        #     data.append(serializer.data)
        serializer= serializers.BookingsSerializer(booking, many=True)
        return Response({"status":"sucess",
                            "booking":serializer.data,},
                            status=200)
    
    def post(self, request, format=None):
        print(request.data)
        # serializer = serializers.RegistrationSerializer(data=request.data)
        if request.data.get('visitor_id') and request.data.get('stall_id') and request.data.get('time') and request.data.get('date') and request.data.get('interest'):
            visitor= get_object_or_404(Visitors, pk=request.data.get('visitor_id'))
            stall= get_object_or_404(Stalls, pk=request.data.get('stall_id'))
            booking= Booking(stall=stall,visitor=visitor,time=request.data.get('time'),date=request.data.get('date'),interest=request.data.get('interest'))
            booking.save()
            return Response({"status":"success",'msg': 'booking successfully'},status=200) 
        return Response({"status":"failed",'msg': 'failed to update user'},status=400)
     

# Visitors login api
@api_view(['GET','POST'])
def visitor_login(request):
    print("Login api")
    if request.method=='POST':
        email= request.POST.get('email')
        password= request.POST.get('password')
        user= authenticate(request,email,password)
        if user:
            visitor= Visitors.objects.get(id=user.id)
            serializer= serializers.VisitorsSerializer(visitor)
            return JsonResponse({"status":"sucess",
                                 "userId":user.id,
                                 "user":serializer.data},
                                 safe=False)
        else:
            return JsonResponse({"status":"faild","msg":"Invalid username or password"})


#Login API
class UsersView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, format=None):
        email= request.data['email']
        password= request.data['password']
        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            serializer= serializers.UsersSerializer(user)
            return Response({
                'token': str(refresh.access_token),
                # 'refresh': str(refresh),
                'user':serializer.data
            })
        return Response({'error': 'Invalid credentials'}, status=400)

class AdminListView(CustomExceptionHandler,APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, requeset, format=None):
        admin= AdminProfile.objects.all()
        serializer= serializers.AdminProfileSerializer(admin, many=True)
        return  JsonResponse({"admin":serializer.data},safe=False)

class VendorListView(CustomExceptionHandler,APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, requeset, pk, format=None):
        admin= AdminProfile.objects.get(id=pk)
        vendor= VendorProfile.objects.filter(admin=admin)
        serializer= serializers.VendorProfileSerializer(vendor, many=True)
        return  JsonResponse({"vendors":serializer.data},safe=False)
    
    # def handle_exception(self, exc):
    # # Override default exception handling to customize the response
    #     if isinstance(exc, AuthenticationFailed):
    #         return Response({'status': 'failed', 'msg': str(exc)}, status=401)
    #     return super().handle_exception(exc)

class VendorDetailView(CustomExceptionHandler,APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, requeset, pk, format=None):
        vendor= VendorProfile.objects.get(id=pk)
        serializer= serializers.VendorProfileSerializer(vendor)
        return  JsonResponse({"vendor":serializer.data},safe=False)
    
    
#get events by location
class EventsByLocationView(CustomExceptionHandler,APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, requeset, city, format=None):
        # with connection.cursor() as cursor:
        #     query="""
        #         SELECT c.cname AS category_name
        #         FROM admin_profile AS a
        #         INNER JOIN categories AS c 
        #         ON a.category = c.id
        #         WHERE a.city = %s
        #     """
        #     cursor.execute(query,[city])
        #     rows = cursor.fetchall()
        #     for row in rows:
        #         print(row[0])
        #     print("data :  ", json.dumps(rows))
        # admin= AdminProfile.objects.all().filter(city=city)
        # joinAdmin= AdminProfile.objects.select_related('category').filter(city=city)
        joinAdmin= AdminProfile.objects.select_related('category').filter(Q(city__iexact=city.lower()))  # Case-insensitive city comparison
        
        serializer= serializers.AdminProfileSerializer(joinAdmin,many=True)
        
        # return JsonResponse({"admin":serializer.data},safe=False)
        return JsonResponse({"admin":serializer.data},safe=False)

    
class RecommendationsStallView(CustomExceptionHandler,APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, id ,format=None):
        stalls= Stalls.objects.all().filter(vendor__admin_id=id).filter(stall_visits__gt=10).order_by('-rating')  
        serializer= serializers.StallsSerializer(stalls, many=True)
        return  JsonResponse({"stalls":serializer.data},safe=False)

class CSVData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, id ,format=None):
        visits= Visits.objects.all().filter(stalls__vendor__admin_id=id)
        serializer= serializers.VisitsRecommendationSerializer(visits, many=True)
        # return  Response({"visits":serializer.data})
         # Create a CSV string in memory
        csv_string = ""
        fields= ['id','visitors_id','stalls_id',"review","rating"]

        # Write the header row
        csv_string += ','.join(fields) + '\n'

        # Write each serialized object data as a row
        for data in serializer.data:
            row_data = [str(value) for value in data.values()]  # Convert all values to strings
            csv_string += ','.join(row_data) + '\n'

        # Create a Django HttpResponse object with CSV content type
        # response = HttpResponse(content_type='text/csv')
        # response.write(csv_string.encode('utf-8'))
        # response['Content-Disposition'] = 'attachment; filename=visit_recommendations.csv'

        return Response({"data":csv_string})


def getSuperuserDashoard( request):
    # visitors= Visits.objects.all().filter(stalls__vendor_id=request.user.vendor_id)
    admin= AdminProfile.objects.all()
    # max_val= admin.count()+2

    today = date.today()  # Get today's date

    # Calculate desired month range (3 previous + 1 next)
    start_month = today.month - 3
    end_month = today.month 

    # Handle month overflow cases (e.g., December + 1 = January of next year)
    if start_month < 1:
        start_month += 12  # Wrap around to previous year if necessary
        start_year = today.year - 1
    else:
        start_year = today.year

    if end_month > 12:
        end_month -= 12  # Wrap around to next year if necessary
        end_year = today.year + 1
    else:
        end_year = today.year
    
    month_labels = [f"{calendar.month_name[month]}" for month in range(start_month, end_month + 1)]
    if start_month != end_month:  # Add next month label if not the same as last month
        month_labels.append(f"{calendar.month_name[end_month + 1]}")
    
    month_counts = [0 for i in month_labels]

    for ad in admin:
        ad_date = ad.created_at.date()
        month = ad_date.month

        # Filter registrations based on desired month range
        if start_year <= ad_date.year <= end_year and start_month <= month <= end_month:
            month_counts[month_labels.index(calendar.month_name[month])] += 1
    

    max_val=max(month_counts)+2


    context={
        "status":"success",
        'labels': month_labels,
        'values': month_counts,
        'max_val': max_val
        }
    return  JsonResponse({"data":context},safe=False)


def getAdminDashoard( request):
    # visitors= Visits.objects.all().filter(stalls__vendor_id=request.user.vendor_id)
    admin= AdminProfile.objects.get(id=request.user.admin_id)
    registrations= Registration.objects.all().filter(admin_id=request.user.admin_id)
    max_val= registrations.count()+2



    start_date = datetime.strptime(admin.start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(admin.end_date, '%Y-%m-%d').date()
    date_list = []

    while start_date <= end_date:
        date_list.append(start_date)
        start_date += timedelta(days=1)
    labels = [date.strftime("%Y-%m-%d") for date in date_list]
    counts = [0 for i in labels]
    for reg in registrations:
        date = reg.created_at.date()
        date = str(date)
        counts[labels.index(date)] += 1
        
    context={
        "status":"success",
        'labels': labels,  # Serialize data for template
        'values': counts,  # Serialize data for template
        'max_val':max_val
        }
    return  JsonResponse({"data":context},safe=False)

def getDashoard( request):
    vendor= VendorProfile.objects.get(id=request.user.vendor_id)
    visitors= Visits.objects.all().filter(stalls__vendor_id=request.user.vendor_id)
    bookings= Booking.objects.all().filter(stall__vendor_id=request.user.vendor_id)
    admin= AdminProfile.objects.get(id=vendor.admin_id)
    max_val= visitors.count()+2



    start_date = datetime.strptime(admin.start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(admin.end_date, '%Y-%m-%d').date()
    date_list = []

    while start_date <= end_date:
        date_list.append(start_date)
        start_date += timedelta(days=1)
    labels = [date.strftime("%Y-%m-%d") for date in date_list]

    
    
    counts = [0 for i in labels]
    bookings_value=[0 for i in labels]

    print("\n\n labels : ",labels,"\n\n")

    for visitor in visitors:
        date = visitor.created_at.date()
        date = str(date)
        counts[labels.index(date)] += 1

    for booking in bookings:
        format_date=booking.date
        l_fd= format_date.split("/")
        format_date= l_fd[2]+"-"+l_fd[1]+"-"+l_fd[0]
        print("\n\n visitor : ",format_date,"---",booking.id,"\n\n")
    
        date = str(format_date)
        bookings_value[labels.index(date)] += 1
            
    context={
        "status":"success",
        'labels': labels,  # Serialize data for template
        'values': counts,  # Serialize data for template
        'bookings': bookings_value,  # Serialize data for template
        'max_val':max_val
        }
    return  JsonResponse({"data":context},safe=False)

def get_booking_by_date(request):
    if request.method == 'GET':
        date= request.GET['selectedDate']
        print("\n\n date : ",date,"\n\n")

        # data = list(Booking.objects.all().filter(date=date).values())
        data = Booking.objects.select_related('visitor').filter(date=date)
        # serializer = serializers.BookingFilterSerializer(data, many=True)
        context=[]
        for booking in data:
            context.append([booking.id,booking.visitor.first_name,booking.visitor.last_name,booking.visitor.contact,booking.visitor.company,booking.interest,booking.time,booking.date,booking.status])
        
        return JsonResponse({'context': context }, status=200)
    return JsonResponse({'status': 'Invalid request'}, status=400)

def get_visits_by_date(request):
    if request.method == 'GET':
        date= request.GET['selectedDate']
        print("\n\n date : ",date,"\n\n")
        l_date= date.split("/")
        date= l_date[2]+"-"+l_date[1]+"-"+l_date[0]
        # date_obj = date(date)
        # date_obj= date_obj.format("%d/%m/%Y")
        # print("\n\n date_obj : ",date_obj,"\n\n")
        stall= Stalls.objects.get(vendor_id=request.user.vendor.id)
        visitors= Visits.objects.select_related('visitors', 'stalls').filter(stalls=stall.id).filter(created_at__startswith=date)
    
        context=[]
        for visitor in visitors:
            context.append([visitor.visitors.first_name,visitor.visitors.last_name,visitor.visitors.contact,visitor.rating,visitor.review,visitor.created_at])
        
        return JsonResponse({'context': context }, status=200)
    return JsonResponse({'status': 'Invalid request'}, status=400)
def group_visitors_by_date(visitors):
    grouped_data = {}
    for visitor in visitors:
        date = visitor.created_at.date()  # Extract date from created_at
        if date not in grouped_data:
            grouped_data[date] = 0
        grouped_data[date] += 1
    return grouped_data

""" Old apis """
'''   
# Create your views here.
@api_view(['GET'])
def demo(request):
    
    return JsonResponse({"status : ","sucess"},safe=False)

@api_view(['GET','POST'])
def usersData(request):
    users= CustomUser.objects.all()
    serializer= serializers.UsersSerializer(users, many=True)
    return  JsonResponse({"users":serializer.data},safe=False)
    # return Response(serializer.data)

@api_view(['GET','POST'])
def login(request):
    if request.method=='POST':
        print("Login api : ",request)
        email= request.POST.get('email')
        password= request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            serializer= serializers.UsersSerializer(user)
            return Response(serializer.data)

# Visitors login
@api_view(['GET','POST'])
def visitor_login(request):
    print("Login api")
    if request.method=='POST':
        email= request.POST.get('email')
        password= request.POST.get('password')
        user= authenticate(request,email,password)
        if user:
            visitor= Visitors.objects.get(id=user.id)
            serializer= serializers.VisitorsSerializer(visitor)
            return JsonResponse({"status":"sucess",
                                 "userId":user.id,
                                 "user":serializer.data},
                                 safe=False)
        else:
            return JsonResponse({"status":"faild","msg":"Invalid username or password"})
#Visitors Registration 
@api_view(['GET','POST'])
def visitor_register(request):
    if request.method=='POST':
        email= request.POST.get('email')
        # password= request.POST.get('password')
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        contact= request.POST.get('contact')
        # en_password= make_password(password) #encrypting the password

        #create the visitor
        visitor= Visitors.objects.create(
            email=email,
            # password= en_password,
            first_name= first_name,
            last_name= last_name,
            contact= contact
        )

        user=CustomUser.objects.create(
                email=email,
                # password= en_password,
                role= "visitor"
            )

        if visitor:
            serializer= serializers.VisitorsSerializer(visitor)        
            # return the user object
            return JsonResponse({"status":"sucess","userId":user.id,
                                "user": serializer.data},
                                safe=False)
        #error while creating the object
        else:
            return JsonResponse({"status":"failed","msg":"User not created"})

@api_view(['GET','POST'])
def admin_reg(request):
    admin= AdminRegister.objects.all()
    serializer= serializers.AdminRegisterSerializer(admin,many=True)
    return JsonResponse({"admin":serializer.data},safe=False) #Response(serializer.data)
    
@api_view(['GET','POST','PUT'])
def admin_reg_details(request,pk):
    admin= get_object_or_404(AdminRegister,pk=pk)
    if request.method=="GET":
        serializer= serializers.AdminRegisterSerializer(admin)
        return JsonResponse({"admin":serializer.data},safe=False)
    elif request.method=="POST":
        pass
    elif request.method=="PUT":
        serializer= serializers.AdminRegisterSerializer(admin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        Response(serializer.error)
    elif request.method=="DELETE":
        admin.objects.delete()
        return JsonResponse({"status":"sucess","msg":"data delected"},safe=False)
        

'''