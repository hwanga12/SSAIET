# accounts/serializers.py
from rest_framework import serializers
from .models import User


# 1) 회원가입용 Serializer ------------------------------------
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# 2) 유저 정보 조회용 Serializer --------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'height',
            'current_weight',
            'target_weight',
            'muscle_mass',
            'body_fat',
            'age',
            'gender',
            'allergies',
        ]


# 3) 프로필 수정(Weight Settings) Serializer ---------------------
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'height',
            'current_weight',
            'target_weight',
            'muscle_mass',
            'body_fat',
            'age',
            'gender',
            'allergies',
        ]
