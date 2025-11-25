from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='아이디'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='이메일'
    )
    first_name = models.CharField(
        max_length=30,
        blank=True
    )
    last_name = models.CharField(
        max_length=30,
        blank=True
    )

    # 신체 정보 필드
    height = models.FloatField(
        null=True,
        blank=True
    )
    current_weight = models.FloatField(
        null=True,
        blank=True
    )
    target_weight = models.FloatField(
        null=True,
        blank=True
    )
    muscle_mass = models.FloatField(
        null=True,
        blank=True
    )
    body_fat = models.FloatField(
        null=True,
        blank=True
    )
    age = models.IntegerField(
        null=True,
        blank=True
    )
    gender = models.CharField(
        max_length=10,
        choices=[('M', '남'), ('F', '여')],
        default='M'
    )

    # 서비스용 정보 필드
    allergies = models.TextField(
        blank=True,
        null=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email