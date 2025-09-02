from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Thread(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Post(models.Model):
    thread = models.ForeignKey(Thread, related_name="posts", on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_first = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["thread", "created_at"]

    def __str__(self):
        return f"Post by {self.author.username} in {self.thread.title}"


class Like(models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")




class Announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MediaItem(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='media/')
    is_image = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        ext = self.file.name.lower().split('.')[-1]
        self.is_image = ext in ['jpg', 'jpeg', 'png', 'gif']
        self.is_video = ext in ['mp4', 'webm', 'ogg']
        super().save(*args, **kwargs)
