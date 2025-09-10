from django.db import models

class GalleryImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Media(models.Model):
    file = models.FileField(upload_to='media/')
    title = models.CharField(max_length=255)
    is_image = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 👈 додай це

    def __str__(self):
        return self.title


