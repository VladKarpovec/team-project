from django.db import models

class Material(models.Model):
    TYPE_CHOICES = [
        ('file', 'Файл'),
        ('image', 'Зображення'),
        ('youtube', 'YouTube відео'),
        ('link', 'Посилання'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    material_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='file')
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
