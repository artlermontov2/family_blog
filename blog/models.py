from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)
    # description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f'/{self.pk}/'

    def __str__(self):
        return self.title
