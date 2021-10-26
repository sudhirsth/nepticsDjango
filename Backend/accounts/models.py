from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, email, password = None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address.')
        
        user = self.model(
            email = self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.staff = True
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password
        """
        user = self.create_user(
            email,
            password=password
        )
        user.staff=True
        user.admin=True
        user.save(using = self._db)
        return user


class User(AbstractBaseUser):    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)   
    profile_image= models.ImageField(
        upload_to='images/',
        default='')
    contact_number = models.CharField(max_length=15)    
    address = models.CharField(max_length = 30)
    is_deleted = models.BooleanField(default=False, editable = False)

    #Account Details
    email = models.EmailField(
        
        verbose_name='email addresss',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)    
    staff = models.BooleanField(default=False)#an admin user; non superuser
    admin = models.BooleanField(default=False) #superuser
    #change later
    is_email_verified = models.BooleanField(default=True)

    # "Password Field" is absent because it is built-in.

    USERNAME_FIELD = 'email' #It replaces the built-in username field for whatever you designate (email in our case).
    REQUIRED_FIELDS = [] #Email and Password are required by default.

    # def get_full_name(self):
    #    fullname= self.first_name+" "+self.last_name
    #    return fullname
    
    def  __str__(self):
        return self.email
        
    def has_perm(self, per, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self,app_labels):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always        
        return True

    @property
    def is_staff(self):
        "Is the user a staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user an admin?"
        return self.admin

    objects = UserManager()

