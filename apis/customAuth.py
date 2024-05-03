from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        if 'Authorization' not in request.headers:
            raise AuthenticationFailed(detail="Please Login", code="no_authentication")
        else:
            auth_header = request.headers['Authorization']
            # Check if the header starts with 'Bearer ' (including the space)
            if auth_header.startswith('Bearer '):
                try:
                    # Attempt to authenticate using JWTAuthentication
                    return super().authenticate(request)
                except:
                    # If JWT authentication fails, check if Authorization header is present
                    if 'Authorization' not in request.headers:
                        raise AuthenticationFailed(detail="Please Login", code="no_authentication")
                    # If Authorization header is present but authentication fails, return None
                    raise AuthenticationFailed(detail="Invalid Token", code="no_authentication")
            else:
                raise AuthenticationFailed(detail="Please Login", code="no_authentication")
        return None
    
class CustomExceptionHandler:
    def handle_exception(self, exc):
        print("\n\nInside CustomExceptionHandler\n\n")
        if isinstance(exc, AuthenticationFailed):
            return Response({'status':'failed', 'msg':str(exc)}, status=401)
        elif exc:
            return Response({'status':'failed', 'msg':str(exc)}, status=401)
            # return Response({'detail': exc.detail}, status=HTTP_401_UNAUTHORIZED)
        return super().handle_exception(exc)


