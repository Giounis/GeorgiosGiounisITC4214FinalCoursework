from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission, Group
from django.db import models
from catalog.models import SavedProduct

class CustomUserManager(BaseUserManager):
    #creates a user
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    #model that creates a superuser
    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True 
        user.is_superuser = True
        user.save(using=self._db)
        return user

#Models for the different kinds of users
class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('user', 'User'),
    )
    
    role = models.CharField(max_length=10, choices=ROLES, default='user')

# Creates groups for Admin, Staff, and User
    admin_group, created = Group.objects.get_or_create(name='Admin')
    staff_group, created = Group.objects.get_or_create(name='Staff')
    user_group, created = Group.objects.get_or_create(name='User')
    email = models.EmailField(unique=True)


    objects = CustomUserManager()

    groups = models.ManyToManyField(Group, blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_user_set')
    saved_products = models.ManyToManyField(SavedProduct, blank=True, related_name='saved_products')
