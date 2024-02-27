from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class Location(models.Model):
    county = models.CharField(max_length = 20)
    sub_county = models.CharField(max_length = 20)
    ward = models.CharField(max_length = 20)

    def __str__(self):
        return self.ward



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # ... normalization of email address, etc. 
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self.db)
        return user
    
class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=20)
    profile_photo = models.ImageField(blank=True, null=True)
    national_id = models.CharField(max_length=12,blank=True, null=True)
    user_types = [("MERCHANT","Merchant"), ("CUSTOMER", "Customer"), ("GROUP", "Group")]
    user_type = models.CharField(max_length= 10, choices=user_types)
    location = models.ForeignKey(Location, on_delete = models.SET_NULL, blank=True, null=True)


    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email.split("@")[0]

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff"
        return self.is_admin



class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length = 300)
    read = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content[:15]