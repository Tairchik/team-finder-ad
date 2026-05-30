from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Пока оставляем пустым, чтобы Django просто увидел класс.
    pass