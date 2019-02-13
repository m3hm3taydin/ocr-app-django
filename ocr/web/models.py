from django.db import models

# Create your models here.
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='images/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    converted_text = models.TextField(blank=True)
