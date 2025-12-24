from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# ============================================================
# 1) 회원가입용 Serializer
# ============================================================
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'name',
        ]

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        # UserManager의 create_user를 호출하여 비밀번호 해싱을 자동으로 처리합니다.
        return User.objects.create_user(**validated_data)


# ============================================================
# 2) 유저 정보 조회용 Serializer
# ============================================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'name',
            'height',
            'current_weight',
            'target_weight',
            'muscle_mass',
            'body_fat',
            'age',
            'gender',
            'allergies',
        ]


# ============================================================
# 3) 프로필 업데이트 Serializer (신체 정보 등)
# ============================================================
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name',
            'height',
            'current_weight',
            'target_weight',
            'muscle_mass',
            'body_fat',
            'age',
            'gender',
            'allergies',
        ]


# ============================================================
# 4) 계정 정보 업데이트 Serializer (아이디, 비밀번호)
# ============================================================
class AccountUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_password(self, value):
        if value:
            validate_password(value)
        return value

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance