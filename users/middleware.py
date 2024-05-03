from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpResponseForbidden,JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("inside middleware **",request.user," : ", request)
        # Custom authentication logic here (if applicable)
        # ...
        if request.path == '/':
            print("\n\n inside / \n")
            return self.get_response(request)
        
        if(request.path.startswith('/logout/')):
            return self.get_response(request)
        if request.path.startswith('/favicon.ico'):
            return self.get_response(request)
        if(request.path.startswith('/api/')):
            return self.get_response(request)
        if(request.path.startswith('/files/')):
            return self.get_response(request)
        
            if request.user.is_authenticated:
                return self.get_response(request)
            else:
                return JsonResponse({"status":"faild","msg":"Please Login"})

        if request.user.is_authenticated:
            if request.user.role=='super' and request.path.startswith('/superuser/'):
                return self.get_response(request)
            elif request.user.role=='admin' and request.path.startswith('/organizer/'):
                return self.get_response(request)
            elif request.user.role=='vendor' and request.path.startswith('/vendor/'):
                return self.get_response(request)
            # elif request.path.startswith('/api/'):
            #     return self.get_response(request)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")


        # # Leverage Django's built-in authentication for standard scenarios
        # if request.user.is_authenticated:
        #     return self.get_response(request)


        
        # Handle authentication attempts (if applicable)
        if request.method == 'POST' and 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect((reverse('superuser_home'))) # Redirect to requested page or default

        # Redirect to login page or handle unauthenticated access as needed
        return redirect('login')#render(request,'login.html',{})

