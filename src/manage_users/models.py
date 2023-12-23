import uuid
from django.contrib.auth.models import AbstractUser

from config.choice import RoleUser
from config.models import BaseModel
from django.db import models

# Create your models here.
class AccountUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField("Role", max_length=50, choices=RoleUser.choices, default=RoleUser.USER)

    def __str__(self) -> str:
        return self.username

