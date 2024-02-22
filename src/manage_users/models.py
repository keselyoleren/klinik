import uuid
from django.contrib.auth.models import AbstractUser

from config.choice import RoleUser
from config.models import BaseModel
from django.db import models
from PIL import Image


# Create your models here.
class AccountUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField("Role", max_length=50, choices=RoleUser.choices, default=RoleUser.USER)
    photo = models.ImageField(upload_to='photo_profile/', null=True, blank=True)

    def __str__(self) -> str:
        return self.username


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.photo:
            img = Image.open(self.photo.path)
            thumbnail_size = (100, 100)  # Set your desired thumbnail size
            img.thumbnail(thumbnail_size)
            img.save(self.photo.path)
