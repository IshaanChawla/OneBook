from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.conf import settings
import datetime

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default = datetime.date.today() + datetime.timedelta(days=1))
      
    def __str__(self):
        return self.user.email
        
class FollowUser(models.Model):
    user_followed = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user_followed')
    user_follower = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user_follower')
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    
    class Meta:
        unique_together = (('user_followed', 'user_follower'),)
                
class CustomUserManager(BaseUserManager):
    def create(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
                email=email,
                is_active = True,
                is_staff = is_staff,
                is_superuser=is_superuser,
                **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        return self.create(email, password, False, False,**extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self.create(email, password, True, True,**extra_fields)
        
        
class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
                'email address',
                max_length=40, 
                unique=True
            )
    full_name = models.CharField(
                max_length=40
            )
    sex = models.CharField(
                max_length=12,
                blank=True
            )
    phone_no = models.CharField(
                max_length=10,
                blank=True
            )
    profile_pic = models.FileField(
                upload_to = 'profile_pics/'
            )
    is_active = models.BooleanField('active', 
                default=True
            )
    is_staff = models.BooleanField('staff status', 
                default=False
            )
    profile_status = models.BooleanField('Profile Status', 
                default=False
            )
    preference_status = models.BooleanField('Preference Status', 
                default=False
            )
    address_on_map = models.BooleanField('Address On Map', 
                default=False
            )
            
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name