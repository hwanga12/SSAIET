# forms.py
from django import forms
from .models import User

    
class WeightSettingsForm(forms.ModelForm):
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

        labels = {
            'height': '현재 키 (cm)',
            'current_weight': '현재 몸무게 (kg)',
            'target_weight': '목표 몸무게 (kg)',
            'muscle_mass': '근육량 (kg)',
            'body_fat': '체지방률 (%)',
            'age': '나이',
            'gender': '성별',
            'allergies': '알레르기 정보'
        }

        widgets = {
            'allergies': forms.Textarea(attrs={'rows': 3})
        }
        
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']

    # 1) 이메일 중복 검사
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 사용 중인 이메일입니다.")
        return email

    # 2) 비밀번호 검증
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
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
            'allergies'
        ]

from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm

class AccountUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']
