from wsgiref.handlers import format_date_time
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def get_pub_date(self):
        pub_date = self.pub_date.strftime("%d-%m-%Y %H:%M:%S")
        return pub_date

    def get_absolute_url(self):
        return reverse('blog:post_details', kwargs={'post_id': self.pk})

    def __str__(self):
        return self.title + " " + self.content 


class Comment(models.Model):
    body = models.TextField()
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    pub_date = models.DateTimeField(auto_now_add=True, )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def get_pub_date(self):
        pub_date = self.pub_date.strftime("%d-%m-%Y %H:%M:%S")
        return pub_date

    def __str__(self):
        return f"{self.body}\nCommented by {self.name} on {self.get_pub_date()}"

    class Meta:
        ordering = ['-pub_date']


    def get_absolute_url(self):
        return reverse('blog:post_details', kwargs={'post_id': self.post_id})

    def get_body(self):
        return self.body

    def get_details(self):
        return f"Commented by {self.name} on {self.get_pub_date()}"