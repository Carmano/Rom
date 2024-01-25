from django.db import models


class Token(models.Model):
    value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

