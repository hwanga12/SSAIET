from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('아이디는 꼭 입력해 주셔야 해요.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='이름')
    
    username_validator = RegexValidator(
        regex=r'^[a-z0-9]+$',
        message='아이디는 영문 소문자와 숫자만 사용 가능해요. 대문자는 쓸 수 없어요.'
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        verbose_name='아이디',
        error_messages={
            'unique': '이미 누가 사용 중인 아이디네요! 다른 걸로 골라보시겠어요?',
        }
    )

    # 📏 키: 0.1 ~ 300cm
    height = models.FloatField(
        null=True, blank=True,
        validators=[
            MinValueValidator(0.1, message='키가 너무 작게 입력되었어요. 다시 확인해 줄래요?'),
            MaxValueValidator(300.0, message='키가 너무 크게 입력되었어요. 다시 확인해 줄래요?')
        ],
        verbose_name='키'
    )
    
    # ⚖️ 현재 체중: 0.1 ~ 500kg
    current_weight = models.FloatField(
        null=True, blank=True,
        validators=[
            MinValueValidator(0.1, message='몸무게는 0보다 커야 정확한 계산이 가능해요.'),
            MaxValueValidator(300.0, message='몸무게 수치가 너무 커요. 다시 확인해 줄래요?')
        ],
        verbose_name='현재 체중'
    )
    
    # 🎯 목표 체중: 0.1 ~ 500kg
    target_weight = models.FloatField(
        null=True, blank=True,
        validators=[
            MinValueValidator(0.1, message='목표 체중을 올바르게 설정해 주세요.'),
            MaxValueValidator(300.0, message='목표 수치가 너무 높아요. 다시 확인해 줄래요?')
        ],
        verbose_name='목표 체중'
    )
    
    # 💪 골격근량: 0 ~ 200kg
    muscle_mass = models.FloatField(
        null=True, blank=True,
        validators=[
            MinValueValidator(0.0, message='근육량은 음수로 입력할 수 없어요.'),
            MaxValueValidator(100.0, message='근육량 수치가 너무 높아요. 다시 확인해 줄래요?')
        ],
        verbose_name='골격근량'
    )
    
    # 📉 체지방률: 0 ~ 100%
    body_fat = models.FloatField(
        null=True, blank=True,
        validators=[
            MinValueValidator(0.0, message='체지방률이 마이너스일 수는 없겠죠?'),
            MaxValueValidator(100.0, message='체지방률은 100%를 넘을 수 없어요.')
        ],
        verbose_name='체지방률'
    )
    
    # 🎂 나이: 1 ~ 150세
    age = models.IntegerField(
        null=True, blank=True,
        validators=[
            MinValueValidator(1, message='나이는 1살 이상부터 입력할 수 있어요.'),
            MaxValueValidator(150, message='나이가 너무 많게 입력되었어요. 다시 확인해 줄래요?')
        ],
        verbose_name='나이'
    )

    gender = models.CharField(
        max_length=10,
        choices=[('M', '남'), ('F', '여')],
        default='M',
        verbose_name='성별'
    )
    
    allergies = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='알레르기 정보'
    )
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username