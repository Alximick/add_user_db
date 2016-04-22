from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=self.normalize_email(username),
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password):
        user = self.create_user(username,
            password=password,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        ('username'),
        max_length=30,
        unique=True,
        # help_text=(
        #     'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        # validators=[
        #     validators.RegexValidator(
        #         r'^[\w.@+-]+$',
        #         ('Enter a valid username. This value may contain only '
        #          'letters, numbers ' 'and @/./+/-/_ characters.')
        #     ),
        # ],
        # error_messages={
        #     'unique': ("A user with that username already exists."),
        # },
    )
    phone_number = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, max_length=10)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
