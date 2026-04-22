from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
 

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, is_active=True, is_staff=False, is_admin=False, is_superuser=False, is_students=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not full_name:
            raise ValueError("Users must have a Fullname")


        user_obj = self.model(
            email = self.normalize_email(email),
            full_name=full_name,
        )
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.superuser = is_superuser
        user_obj.students = is_students
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj


    def create_staffuser(self, full_name, email, password=None):
        user = self.create_user(
                email,
                full_name,
                password=password,
                is_staff=True
        )
        return user

    def create_admin(self, full_name, email, password=None):
        user = self.create_user(
                email,
                full_name,
                password=password,
                is_admin=True
        )
        return user
    
    def create_superuser(self, full_name, email, password=None):
        user = self.create_user(
                email,
                full_name,
                password=password,
                is_staff=True,
                is_admin=True,
                is_students=True,
                is_superuser=True,
        )
        return user


    def create_students(self, full_name, email, password=None):
        user = self.create_user(
                email,
                full_name,
                password=password,
                is_students=True,
                
        )
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    full_name   = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a non super-user
    admin = models.BooleanField(default=False) # an admin
    superuser = models.BooleanField(default=False) # a superuser
    students = models.BooleanField(default=False) # a student user
    
    date_joined = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True, null=True, blank=True)

    # notice the absence of a "Password field", that is built in.


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name',] # Email & Password are required by default.
    
    objects = UserManager()
    
    def __str__(self):          
        return self.email


    def get_full_name(self):
        # The user is identified by their email address
        return self.email


    def get_short_name(self):
        # The user is identified by their email address
        return self.email


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True


    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff


    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_students(self):
        "Is the user a students member?"
        return self.students

    @property
    def is_superuser(self):
        "Is the user a superuser member?"
        return self.superuser

    @property
    def is_active(self):
        "Is the user active?"
        return self.active