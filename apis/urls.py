from django.urls import path
from . import views

urlpatterns = [
    # path('api/demo/',views.demo,name='demo_api'),
    # path('api/password_demo',views.PasswordDemo.as_view(),name='password_demo'),
    
    #visitor 
    path('api/register',views.VisitorsRegistrationView.as_view(),name='register_api'),
    path('api/login',views.VisitorsLoginView.as_view(),name='visitor_login'),
    path('api/visitor/<int:pk>',views.VisitorsView.as_view(),name='update_visitor'),
    path('api/visitors/<int:pk>',views.VisitorsView.as_view(),name='get_visitor_details'),
    path('api/visitors',views.VisitorsView.as_view(),name='get_visitor'),
    
    path('api/organizer/<str:city>',views.EventsByLocationView.as_view(),name='get_events_by_location'),

    #get stall
    path('api/get_stall/<int:id>',views.StallView.as_view(),name='get_stalls'),    

    #send ratings
    path('api/stall_rating',views.VisitorStallRatingView.as_view(),name='visitor_rating'),

    #stall visit
    path('api/stall_visit',views.VisitorStallVisitView.as_view(),name='stall_visit'),

    #registration
    path('api/registration/<int:visitor_id>',views.ExhibitionRegistrationView.as_view(),name='get_registration'),
    path('api/registration',views.ExhibitionRegistrationView.as_view(),name='add_registration'),

    #wishlist
    path('api/wishlist/<int:visitor_id>',views.WishlistView.as_view(),name='get_wishlist'),
    path('api/wishlist',views.WishlistView.as_view(),name='add_wishlist'),
    
    #booking
    path('api/booking/<int:visitor_id>',views.BookingView.as_view(),name='get_booking'),
    path('api/booking',views.BookingView.as_view(),name='add_booking'),
    path('api/booking/bydate',views.get_booking_by_date,name='filter_booking'),
    
    
    #visits
    path('api/visits/bydate',views.get_visits_by_date,name='filter_visits'),
    

    #recommend
    path('api/recommend',views.RecommendationsStallView.as_view(),name='recommend_stall'),
    path('api/CSVData/<int:id>',views.CSVData.as_view(),name='recommend_stall_model'),
    path('api/GetDataFromDB',views.GetDataFromDB.as_view(),name='GetDataFromDB'),
    

    path('api/dashboard',views.getDashoard,name='dashboard'),
    path('api/dashboard/admin',views.getAdminDashoard,name='admin_dashboard'),
    path('api/dashboard/superuser',views.getSuperuserDashoard,name='superuser_dashboard'),
    

    path('api/token-auth/', views.UsersView.as_view() , name='api_token_auth'),
    path('api/getAdmins', views.AdminListView.as_view() , name='getAdmins'),
    
    path('api/getVendors/<int:pk>', views.VendorListView.as_view() , name='getVendors'),
    path('api/getVendor/<int:pk>', views.VendorDetailView.as_view() , name='getVendor'),

    #top categories
    path('api/top_categories',views.TopCategory.as_view(),name='top_categories'),

    # path('api/users/',views.usersData,name='users_api'),
    # path('api/login/',views.login,name='login_api'),
    # path('api/admin_reg/',views.admin_reg,name='admin_reg'),
    # path('api/visitor_register/',views.visitor_register,name='visitor_register'),
    # path('api/visitor_login/',views.visitor_login,name='visitor_login'),
    # path('api/admin_reg_details/<int:pk>',views.admin_reg_details,name='admin_reg_details'),
]
