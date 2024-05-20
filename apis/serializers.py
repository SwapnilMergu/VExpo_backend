from rest_framework import serializers
from users.models import CustomUser
from admin_profile.models import AdminProfile
from categories.models import Categories
from vendor_profile.models import VendorProfile
from visitors.models import Visitors
from visits.models import Visits
from django.contrib.auth.hashers import make_password
from booking.models import Booking
from stalls.models import Stalls
from wishlist.models import Wishlist
from registration.models import Registration
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields= ['id','email','role','vendor_id','admin_id']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Categories
        fields= ['id','cname']

class AdminProfileSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='cname', queryset=Categories.objects.all())  # Related field

    class Meta:
        model= AdminProfile
        # fields= ['id','event_name','contact','email','password','address', 'city', 'logo', 'category','catalog','DOB','whatsapp_no','social_links','about','status']
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}} 



class VendorProfileSerializer(serializers.ModelSerializer):
    # category = serializers.SlugRelatedField(slug_field=['id','cname'], queryset=Categories.objects.all())  # Related field
    admin = AdminProfileSerializer(read_only=True)  # Nested serializer with read-only option
    class Meta:
        model= VendorProfile
        fields= '__all__'

class VisitorsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Visitors
        fields= ['id','email','first_name','last_name','contact',"company"]

class RegistrationSerializer(serializers.ModelSerializer):
    # category = serializers.SlugRelatedField(slug_field='cname', queryset=AdminProfile.objects.all())  # Related field
    # admin_id = serializers.SlugRelatedField(slug_field='event_name', queryset=AdminProfile.objects.all())  # Related field
    admin = AdminProfileSerializer(read_only=True)  # Nested serializer with read-only option
    visitor = VisitorsSerializer(read_only=True)  # Nested serializer with read-only option
    class Meta: 
        model= Registration
        fields = '__all__'

class WishlsitSerializer(serializers.ModelSerializer):
    visitor = VisitorsSerializer(read_only=True)  # Nested serializer with read-only option
    admin  = AdminProfileSerializer(read_only=True)  # Nested serializer with read-only option
    class Meta:
        model= Wishlist
        fields= '__all__'
    
class StallsSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True) #serializers.SlugRelatedField(slug_field=['id','cname'], queryset=Categories.objects.all())
    vendor = VendorProfileSerializer(read_only=True)  # Nested serializer with read-only option
    class Meta:
        model= Stalls
        fields= '__all__'

class VisitsSerializer(serializers.ModelSerializer):
    visitor = VisitorsSerializer(read_only=True)  # Nested serializer with read-only option
    stalls  = StallsSerializer(read_only=True)  # Nested serializer with read-only option
    class Meta:
        model= Visits
        fields= '__all__' #['id','visitor_id',"stall_id","review","rating"]

class VisitsRecommendationSerializer(serializers.ModelSerializer):
    # visitor = VisitorsSerializer(read_only=True)  # Nested serializer with read-only option
    # stalls  = StallsSerializer(read_only=True)  # Nested serializer with read-only option
    # visitor_id = serializers.SlugRelatedField(slug_field='id', queryset=Visitors.objects.all())  # Related field
    # stall_id = serializers.SlugRelatedField(slug_field='id', queryset=Stalls.objects.all())  # Related field

    class Meta:
        model= Visits
        fields= ['id','visitors_id','stalls_id',"review","rating"]

        
class BookingsSerializer(serializers.ModelSerializer):
    visitor = VisitorsSerializer(read_only=True)  # Nested serializer with read-only option
    stall= StallsSerializer(read_only=True)  # Nested serializer with read-only option   
    class Meta:
        model= Booking
        fields= '__all__'


class VisitorLoginSerializer(TokenObtainPairSerializer):
    pass  # Inherit from TokenObtainPairSerializer for login

class BookingFilterSerializer(serializers.Serializer):
    # visitor_first_name = serializers.SlugRelatedField(slug_field='first_name', queryset=Visitors.objects.all(), required=False)
    # visitor_last_name = serializers.SlugRelatedField(slug_field='last_name', queryset=Visitors.objects.all(), required=False)
    # visitor_contact = serializers.SlugRelatedField(slug_field='contact', queryset=Visitors.objects.all(), required=False)

    class Meta:
        model = Booking
        fields = ['id',  'date', 'time', 'interest', 'status']

#booking api
class BookingAPISerializer(serializers.Serializer):
    visitor= VisitorsSerializer(read_only=True)  # Nested serializer with read-only option
    vendor= VendorProfileSerializer(read_only=True)  # Nested serializer with read-only option
    class Meta:
        model = Booking
        fields = '__all__'