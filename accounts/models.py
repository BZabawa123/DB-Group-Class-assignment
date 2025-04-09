from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsersManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(max_length=80, unique=True)
    password = models.CharField(max_length=100)
    USER_ROLES = (
        ('SuperAdmin', 'SuperAdmin'),
        ('Admin', 'Admin'),
        ('Student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    objects = UsersManager()

    class Meta:
        db_table = 'Users'

# # accounts/models.py
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models

# class UsersManager(BaseUserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('Users must have an email address')
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(username, email, password, **extra_fields)

# class Users(AbstractBaseUser, PermissionsMixin):
#     uid = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=80, unique=True)
#     email = models.EmailField(max_length=80, unique=True)
#     password = models.CharField(max_length=100)
#     USER_ROLES = (
#         ('SuperAdmin', 'SuperAdmin'),
#         ('Admin', 'Admin'),
#         ('Student', 'Student'),
#     )
#     role = models.CharField(max_length=10, choices=USER_ROLES)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     REQUIRED_FIELDS = ['email']
#     USERNAME_FIELD = 'username'

#     objects = UsersManager()

#     class Meta:
#         db_table = 'Users'