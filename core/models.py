from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
# Create your models here.

class UserManager(BaseUserManager): 

    def create_user(self, username, firstname, email, lastname, password=None, commit=True):
        
        if not username:
            raise ValueError(_('Users must be have an email'))
        if not firstname:
            raise ValueError(_('Users must be have an firstname')) 
        if not lastname:
            raise ValueError(_('Users must be have an lastname'))
        if not email:
            raise ValueError(_('Users must be have an email'))  

        user = self.model(
            username=username,
            email = self.normalize_email(email),
            firstname = firstname,
            lastname=lastname,
        )
        user.set_password(password)
        if commit:
            user.save(using=self._db)

    def create_superuser(self, username, password, email, lastname, firstname):
        user = self.create_user(
            username=username,
            email=email,
            lastname=lastname,
            firstname=firstname,
            password=password,
        )

        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=255, primary_key=True, default=uuid4, unique=True)
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True
    )
    firstname = models.CharField(
        verbose_name=_('first name'),
        max_length=255,
        blank=True
    )
    lastname = models.CharField(
        verbose_name=_('first name'),
        max_length=255,
        blank=True
    )
    username = models.CharField(
        verbose_name=_('username'),
        max_length=255,
        unique=True,
        null=False,
    ),
    password = models.CharField(
        verbose_name=_('password'),
        max_length=255,
        null=False,
    ),
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        auto_now_add=True
    )


    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.firstname, self.lastname)
        return full_name.strip()

    def __str__(self):
        return '{} {}'.format(self.username)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
