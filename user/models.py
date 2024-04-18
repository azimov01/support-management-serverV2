from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import  BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken


from user.constant import DefaultAbstract



#--------------------------#
#      User Manager        #
#__________________________#

class UsManager(BaseUserManager):
    def create_user(self, email,  password, is_staff=False, is_active=True, **extra_fields):
        if not email:
            raise ValueError("The given must be set")
     
        user = self.model(email=email, is_staff=is_staff, is_active=is_active, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email=None, password=None, **extra_fields):
        return self.create_user(email, password, is_staff=True, is_superuser=True, **extra_fields)



#-----------------#
#      User       #
#_________________#
class User(AbstractBaseUser,  PermissionsMixin, DefaultAbstract):
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user_type = models.SmallIntegerField(choices=[
        (1, "Admin"),
        (2, "SuperAdmin"),
        (3, "Operator"),
    ], default=1)
    is_staff = models.BooleanField('Staff', default=False)
    is_active = models.BooleanField('Active', default=True)
    is_superuser = models.BooleanField(default=True)


    def __str__(self) -> str:
        return  f"{self.email} - {self.first_name}"


    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access' :str(refresh.access_token)
        }

    objects = UsManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


# class Token(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     token = models.CharField(max_length=2000)

#     def __str__(self) -> str:
#         return f"{self.user}"