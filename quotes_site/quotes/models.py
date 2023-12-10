from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


class Author(models.Model):
    fullname = models.CharField(max_length=255, blank=False, null=False)
    born_date = models.CharField(max_length=100, blank=True, null=True)
    born_location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.fullname}"


class Quote(models.Model):
    tags = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.quote}"
