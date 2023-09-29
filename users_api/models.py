import uuid
from django.db import models


class User(models.Model):
    uuid_ref = models.UUIDField('UUID Reference', default=uuid.uuid4, editable=False,
                                primary_key=True)   # unique identifiers used as the primary key
    username = models.CharField('Name of user', max_length=255, null=True, blank=True)
    email = models.EmailField('Email', unique=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email
