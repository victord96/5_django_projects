from django.db import models
from django.urls import reverse
from django.conf import settings

from ckeditor.fields import RichTextField


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, default="no category")

    def get_absolute_url(self):
        return reverse('blog:index')

    def __str__(self):
        return self.name        


class Post(models.Model):
    title = models.CharField(max_length=200)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    content = RichTextField(blank=True, null=True)
    pub_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def get_pub_date(self):
        pub_date = self.pub_date.strftime("%d-%m-%Y %H:%M:%S")
        return pub_date

    def get_pub_date_no_hours(self):
        pub_date = self.pub_date.strftime(" %d %B, %Y")
        return pub_date    

    def get_absolute_url(self):
        return reverse('blog:post_details', kwargs={'post_id': self.pk})

    def __str__(self):
        return self.title + " " + self.content 

    def to_url(self, pub_date):
        pub_date = self.pub_date.strftime(" %d %B, %Y")
        return pub_date  


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