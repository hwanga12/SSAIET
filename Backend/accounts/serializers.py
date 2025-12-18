# accounts/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'name',
        ]

    # 🔥 여기 추가 (핵심)
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            # Django ValidationError → DRF ValidationError로 변환
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data.get('name'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# ============================================================
# 2) 유저 정보 조회용 Serializer (UserSerializer)
# ============================================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'name',                   # 🔥 name 추가
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
# 3) 프로필 업데이트 Serializer (ProfileUpdateSerializer)
# ============================================================
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name',                   # 🔥 name도 프로필 수정 가능
            'height',
            'current_weight',
            'target_weight',
            'muscle_mass',
            'body_fat',
            'age',
            'gender',
            'allergies',
        ]

class AccountUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        if 'username' in validated_data:
            instance.username = validated_data['username']

        if 'email' in validated_data:
            instance.email = validated_data['email']

        if 'password' in validated_data and validated_data['password']:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance
