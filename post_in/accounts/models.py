from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
    DateTimeField,
)
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self,
                     email,
                     password=None,
                     name=None,
                     full_name=None,
                     is_active=None,
                     is_staff=None,
                     is_admin=None):
        """Создает и сохраняет пользователя"""
        if not email:
            raise ValueError('Пользователь обязательно должен внести адрес почты')
        if not password:
            raise ValueError('Пользователь обязательно должен внести пароль')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("SuperUser must have is_staff = True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("SuperUser must have is_superuser = True")

        return self._create_user(username, email, password, **extra_fields)


# Create your models here.
class User(AbstractBaseUser):
    email = EmailField(unique=True, max_length=255)
    name = CharField(max_length=255,blank=True,null=True)
    full_name = CharField(max_length=255, blank=True, null=True)
    staff = BooleanField(default=False)
    is_active = BooleanField(default=False)
    admin = BooleanField(default=False)
    timestamp = DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
