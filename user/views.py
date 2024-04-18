from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from django.contrib.auth import logout
from rest_framework.permissions import IsAdminUser, BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly

from user.serializer import UserLoginSerializer, UserRegisterSerializer

from .models import User

class UserWritePermission(BasePermission):
    message = 'Adding customers not allowed.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

@swagger_auto_schema(method="POST", tags=['user'], request_body=UserRegisterSerializer)
@api_view(['POST'])
# @permission_classes([DjangoModelPermissionsOrAnonReadOnly])
def registratsiya(request, *args, **kwargs):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)   
    serializer.save()
    return Response({
        'status' : True,
        "data" : serializer.data,
        
    })  
def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)


@swagger_auto_schema(method="POST", tags=['user'], request_body=UserLoginSerializer)
@api_view(["POST"])
def user_login(request, *args, **kwargs):
    email = request.data['email']
    password = request.data['password']
    user = User.objects.filter(email=email).first()
    if not user or not user.check_password(password):
        return Response({
            "status" : False,
            'error' : "User not found"
        }, status=HTTP_400_BAD_REQUEST)
    user_tokens = user.tokens()


    return Response({
        "status" : True,
        "email": email,
        "password" : password,
        "access_token" : user_tokens.get('access'),
        "refresh_token" : user_tokens.get('refresh') 
    })
  

    

class UserLagout(APIView):
    def post(request):
        logout(request)
        return redirect("login")
    
