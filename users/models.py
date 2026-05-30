import random
import uuid
from io import BytesIO

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont


AVATAR_COLORS = [
    '#5B8DEF', '#9B59B6', '#E67E22',
    '#27AE60', '#E74C3C', '#16A085',
    '#2980B9', '#8E44AD', '#D35400',
]


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name,
                          surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, surname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to='avatars/', default='')
    phone = models.CharField(max_length=12, default='')
    github_url = models.URLField(blank=True)
    about = models.TextField(blank=True, max_length=256)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    favorites = models.ManyToManyField(
        'projects.Project',
        blank=True,
        related_name='interested_users',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def __str__(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        # Генерируем аватар только при создании нового пользователя
        if not self.pk and not self.avatar:
            self.avatar = self._generate_avatar()
        super().save(*args, **kwargs)

    def _generate_avatar(self):
        size = 100
        color = random.choice(AVATAR_COLORS)
        letter = self.name[0].upper() if self.name else '?'

        img = Image.new('RGB', (size, size), color=color)
        draw = ImageDraw.Draw(img)

        # Пробуем загрузить шрифт, если нет — используем дефолтный
        try:
            font = ImageFont.truetype(
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
        except Exception:
            font = ImageFont.load_default()

        # Центрируем букву
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (size - text_w) / 2 - bbox[0]
        y = (size - text_h) / 2 - bbox[1]
        draw.text((x, y), letter, fill='white', font=font)

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'avatar_{uuid.uuid4()}.png'
        return ContentFile(buffer.getvalue(), name=filename)
