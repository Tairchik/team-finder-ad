import re

from django import forms
from django.contrib.auth import authenticate

from users.models import User


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=124)
    surname = forms.CharField(max_length=124)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже существует')
        return email

    def save(self):
        data = self.cleaned_data
        return User.objects.create_user(
            email=data['email'],
            name=data['name'],
            surname=data['surname'],
            password=data['password'],
        )


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError('Неверный имейл или пароль')
            cleaned_data['user'] = user
        return cleaned_data


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']
        widgets = {
            'avatar': forms.FileInput(),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if not phone:
            return phone

        # Приводим 8... к +7...
        if re.match(r'^8\d{10}$', phone):
            phone = '+7' + phone[1:]
        elif not re.match(r'^\+7\d{10}$', phone):
            raise forms.ValidationError(
                'Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX')

        # Проверка уникальности (исключаем текущего пользователя)
        qs = User.objects.filter(phone=phone)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Этот номер телефона уже используется')

        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url', '')
        if url and 'github.com' not in url:
            raise forms.ValidationError('Ссылка должна вести на GitHub')
        return url


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(
        widget=forms.PasswordInput, label='Новый пароль')
    new_password2 = forms.CharField(
        widget=forms.PasswordInput, label='Подтверждение пароля')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Неверный текущий пароль')
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password1')
        p2 = cleaned_data.get('new_password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data

    def save(self):
        self.user.set_password(self.cleaned_data['new_password1'])
        self.user.save()
